from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
# from django.conf.urls.static import static
# from . import settings

urlpatterns = [
    path("", include('myapp.urls')),# Handles user home/dashboard 
    # path('blog/', include('blog.urls')),  # Blog-specific routes
    path('blog/', include('blog.urls', namespace='blog')),  # ✅ register namespace
    # path("accounts/", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
