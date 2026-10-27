"""
URL configuration for rental project.
"""
from app.views import service_worker
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView, TemplateView
from django.templatetags.static import static as static_url
from django.contrib.sitemaps.views import sitemap as sitemap_view
from rental.sitemaps import sitemaps

urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'favicon.ico',
        RedirectView.as_view(
            url=settings.STATIC_URL + 'images/Hemoaid_logo1.png',
            permanent=True
        ),
    ),

    # Robots.txt
    path(
        'robots.txt',
        TemplateView.as_view(template_name='robots.txt', content_type='text/plain'),
        name='robots_txt',
    ),

    # XML Sitemap
    path(
        'sitemap.xml',
        sitemap_view,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap',
    ),

    # Service Worker
    path(
        "service-worker.js",
        service_worker,
        name="service_worker",
    ),

    # App URLs
    path('', include('app.urls')),

    # Social Auth
    path('auth/', include('social_django.urls', namespace='social')),
]

import os
from django.urls import re_path
from django.views.static import serve as static_serve
from django.shortcuts import redirect

def serve_media(request, path):
    full_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(full_path):
        return static_serve(request, path, document_root=settings.MEDIA_ROOT)
    bucket = getattr(settings, 'GS_BUCKET_NAME', 'quicknest-media-2026') or 'quicknest-media-2026'
    return redirect(f"https://storage.googleapis.com/{bucket}/{path}")

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve_media),
]