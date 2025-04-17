

from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import BlogPost, BlogLike, BlogComment
from myapp.models import CustomUser
from django.contrib import messages
from django.db.models import Prefetch
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # only if you use fetch without CSRF

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import BlogPost, BlogComment



from django.core.paginator import Paginator
from django.utils.timesince import timesince



@login_required
def blog_feed(request):
    user_type_filter = request.GET.get('user_type')
    post_id_filter = request.GET.get('post_id')  # Get post_id if available

    if not user_type_filter:
        user_type_filter = "my_posts"  # default to logged-in user's posts

    # Get posts based on user type
    if user_type_filter == "my_posts":
        posts = BlogPost.objects.filter(author=request.user).select_related('author', 'shared_post').prefetch_related('likes', 'comments')
    elif user_type_filter in ["1", "2", "3"]:
        queryset = BlogPost.objects.filter(author__user_type=user_type_filter)
        if request.user.user_type != "1":
            queryset = queryset.exclude(author=request.user)
        posts = queryset.select_related('author', 'shared_post').prefetch_related('likes', 'comments')
    else:
        return redirect("login")

    # Add 'is_liked' flag
    for post in posts:
        post.is_liked = post.likes.filter(user=request.user).exists()

    # Choose template
    template = {
        "1": 'admin/home.html',
        "2": 'hospital/home.html',
        "3": 'donor/home.html'
    }.get(request.user.user_type, 'login')

    # If post_id is provided, focus on that post
    if post_id_filter:
        posts = posts.filter(id=post_id_filter)

    return render(request, template, {
        'posts': posts,
        'user_type_filter': user_type_filter
    })



@login_required
def comment_on_post(request, post_id):
    if request.method == "POST":
        content = request.POST.get('content')  # Get content from the form
        if not content:
            return JsonResponse({'success': False, 'error': 'Comment cannot be empty'})

        try:
            post = BlogPost.objects.get(id=post_id)  # Get the post object by ID
        except BlogPost.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post not found'})

        # Create a new comment and associate it with the post and user
        comment = BlogComment.objects.create(
            post=post,
            user=request.user,
            content=content
        )

        # Return the new comment details in JSON format to be rendered on the frontend
        return JsonResponse({
            'success': True,
            'content': comment.content,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'user_type': request.user.get_user_type_display(),
            'profile_pic': request.user.profile_pic.url if request.user.profile_pic else ''
        })
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})





# AJAX: Get paginated comments
@login_required
def get_comments(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    page = int(request.GET.get("page", 1))
    comments = post.comments.all().order_by("-commented_at")  # Most recent first

    paginator = Paginator(comments, 5)
    page_obj = paginator.get_page(page)

    data = [{
        "content": c.content,
        "first_name": c.user.first_name,
        "last_name": c.user.last_name,
        "user_type": c.user.get_user_type_display(),
        "profile_pic": c.user.profile_pic.url if c.user.profile_pic else "",
        "time_since": timesince(c.commented_at),
    } for c in page_obj.object_list]

    return JsonResponse({
        "comments": data,
        "has_next": page_obj.has_next()
    })







@login_required
def delete_post(request, post_id):
    # Retrieve the post, or return a 404 if not found
    post = get_object_or_404(BlogPost, id=post_id)

    # Ensure the logged-in user is the author
    if post.author == request.user:
        post.delete()  # Delete the post if the user is the author
        
        # Redirect to the home page after deletion
        return redirect(reverse('home'))  # Ensure this matches your URL pattern name for the home page
    else:
        raise Http404("You are not authorized to delete this post.")  # Unauthorized access

# @login_required
# def blog_feed(request):
#     # Fetch all posts, and filter by user type in the template
#     posts = BlogPost.objects.select_related('author', 'shared_post').prefetch_related('likes', 'comments')

#     for post in posts:
#         post.is_liked = post.likes.filter(user=request.user).exists()

#     return render(request, 'blog/blog_feed.html', {'posts': posts})





from django.utils.html import strip_tags

@login_required
def create_post(request):
    # Get the user_type of the logged-in user
    user_type = request.user.user_type

    if request.method == "POST":
        caption = request.POST.get('caption')
        image = request.FILES.get('image')

        # Check for valid caption
        if not caption:
            messages.error(request, "Caption is required!")
            return redirect('blog:create_post')

        # Store the raw HTML caption
        BlogPost.objects.create(
            author=request.user,
            caption=caption,  # Store the raw HTML version
            image=image
        )

        messages.success(request, "Post created successfully!")
        return redirect('blog:blog_feed')

    return render(request, 'blog/create_post.html', {'user_type': user_type})




from django.http import JsonResponse

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    like, created = BlogLike.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        "liked": liked,
        "like_count": post.likes.count()
    })






# @login_required
# def user_blog_profile(request, user_id):
#     user = CustomUser.objects.get(id=user_id)
#     posts = BlogPost.objects.filter(author=user).select_related('author')

#     return render(request, 'blog/user_blog_profile.html', {
#         'user': user,
#         'posts': posts
#     })

@login_required
def user_blog_profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    posts = BlogPost.objects.filter(author=user)

    # Pass user_type to the template
    user_type = request.user.user_type  # Get the logged-in user's type

    return render(request, 'blog/user_blog_profile.html', {
        'user': user,
        'posts': posts,
        'user_type': user_type,  # Pass user_type to decide which base template to use
    })
    
@login_required
def post_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    comments = BlogComment.objects.filter(post=post).order_by('commented_at')

    # Get the user_type of the logged-in user
    user_type = request.user.user_type

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'user_type': user_type
    })
@login_required
def share_post(request, post_id):
    original_post = BlogPost.objects.get(id=post_id)
    
    if request.method == "POST":
        caption = request.POST.get('caption')
        
        # Create the new post as a shared post
        BlogPost.objects.create(
            author=request.user,
            caption=caption,
            shared_post=original_post
        )
        
        messages.success(request, "Post shared successfully!")
        return redirect('blog:blog_feed')

    return render(request, 'blog/share_post.html', {
        'original_post': original_post
    })