
from django.db import models
from django.utils import timezone
from myapp.models import CustomUser

from cloudinary.models import CloudinaryField

# ---------------------------
# Blog Post Model (Supports Reposts)
# ---------------------------
class BlogPost(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blog_posts')
    caption = models.TextField(verbose_name="Caption / Description", blank=True)
    image = models.ImageField(upload_to='blog/images/', null=True, blank=True)
    # image = CloudinaryField('image', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    # 🔁 Internal Share (repost)
    shared_post = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='shared_by')

    class Meta:
        ordering = ['-created_at']  # Show latest posts first

    def __str__(self):
        if self.shared_post:
            return f"{self.author.email} shared Post {self.shared_post.id}"
        return f"{self.author.email}'s post at {self.created_at.strftime('%Y-%m-%d')}"

    def is_shared(self):
        return self.shared_post is not None

    def like_count(self):
        return self.likes.count()

    def comment_count(self):
        return self.comments.count()

# ---------------------------
# Blog Like Model (One like per user per post)
# ---------------------------
class BlogLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='liked_posts')
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='likes')
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-liked_at']

    def __str__(self):
        return f"{self.user.email} liked Post {self.post.id}"

# ---------------------------
# Blog Comment Model (Threaded)
# ---------------------------
class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    commented_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['commented_at']

    def __str__(self):
        return f"Comment by {self.user.email} on Post {self.post.id}"

    def is_reply(self):
        return self.parent is not None

