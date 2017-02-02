"""restapi_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from posts import views as posts_views
from accounts.views import (login_view, register_view, logout_view)
from posts.api import urls as posts_api_urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', posts_views.home, name="home"),
    url(r'^create/$', posts_views.post_create, name='create'),
    url(r'^login/', login_view, name='login'),
    url(r'^register/', register_view, name='register'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^api/posts/', include(posts_api_urls, namespace='posts-api')),

    url(r'^(?P<slug>[\w-]+)/$', posts_views.post_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', posts_views.post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', posts_views.post_delete, name='delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)