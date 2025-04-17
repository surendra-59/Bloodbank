from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
# from django.conf.urls.static import static
# from . import settings


urlpatterns = [
    path("", include('myapp.urls')),  # Handles user home/dashboard
    path('blog/', include('blog.urls', namespace='blog')),  # Blog-specific routes with namespace
    path('admin/', admin.site.urls),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
