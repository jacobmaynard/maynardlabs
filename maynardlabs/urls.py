from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
import maynardlabs.views as views

urlpatterns = [
    # Examples:
    url(r'^$', views.index),
    url(r'home/', views.index),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', views.blog),
    url(r'^podcasts/', views.podcast),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^members/login', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
    url(r'^members/logout', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^members/manageprofile', views.profile),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^blogview/', views.blogview),
]
