from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from maynardlabs.models import Blog, Podcast, Image, VidMbed, Profile


class BlogAdmin(admin.ModelAdmin):
    fields = ('title', 'author', 'pubdate', 'lastmod', 'tags', 'status', 'image', 'content', 'hitcount', 'sharedcount')


class PodcastAdmin(admin.ModelAdmin):
    fields = ('title', 'pubdate', 'guests', 'tags', 'status', 'recording', 'runtime', 'filesize', 'image', 'hitcount', 'sharedcount')


class ImageAdmin(admin.ModelAdmin):
    fields = ('name', 'file')


class ProfileAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'email', 'bio', 'birth_day', 'phone_number', 'address', 'podcast_guest')


class VidMbedAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass


admin.site.register(Blog)
admin.site.register(Podcast)
admin.site.register(Image)
admin.site.register(Profile)
admin.site.register(VidMbed, VidMbedAdmin)