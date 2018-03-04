import datetime

import StringIO
from PIL import Image as IMG
from ckeditor.fields import RichTextField
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from embed_video.fields import EmbedVideoField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=2500, null=True, blank=True)
    birth_day = models.TextField(max_length=250, null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    address = models.TextField(max_length=1000, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def getName(self):
        return self.user.first_name + " " + self.user.last_name

    def getBirthDay(self):
        return self.birth_day

    def setPhoneNumber(self, contactinfo):
        self.phone_number = contactinfo
        try:
            self.save()
        except:
            return 0
        return 1

    def getContactInfo(self):
        return self.phone_number


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Question(models.Model):
    text = models.CharField(max_length=200, null=False, blank=False)
    pubdate = models.DateTimeField('date published')
    
    def __unicode__(self):
        return self.text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=7)
    
class Choice(models.Model):
    question = models.ForeignKey('Question')
    choicetext = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __unicode__(self):
        return self.choicetext
    def incrementVotes(self):
        self.votes = self.votes + 1
        self.save()

class Blog(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False, unique=True)
    author = models.ForeignKey('auth.User')
    pubdate = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    lastmod = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    tags = models.CharField(max_length=256, blank=False, null=False)
    status = models.CharField(max_length=24, blank=False, null=False, choices=[('draft','drafting'), ('edit','editor'), ('publish','published')])
    image = models.ForeignKey('Image')
    content = RichTextField(max_length=20971520)
    hitcount = models.IntegerField(default=0)
    sharedcount = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

    def updateHitCount(self):
        self.hitcount = self.hitcount + 1

    def updateSharedCount(self):
        self.sharedcount = self.sharedcount + 1

    def getTitle(self):
        return self.title

    def getPubDate(self):
        return self.pubdate

    def updateLastModified(self):
        self.lastmod = datetime.now()

    class Meta:
        ordering = ['-pubdate']
    
class Image(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    file = models.ImageField(upload_to='images/', blank=False)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id and not self.file:
            return

        img = IMG.open(self.file)
        (width, height) = img.size
        """Max Width and Height 960 X 480"""
        if width > 960:
            width = 960
        if height > 480:
            height = 480
        resolution = (width, height)
        tempimage = img.resize(resolution, IMG.ANTIALIAS)
        tempimage_io = StringIO.StringIO()
        tempimage.save(tempimage_io, format='JPEG')
        image_file = InMemoryUploadedFile(tempimage_io, None, self.name + '.jpg', 'image/jpeg', tempimage_io.len, None)
        self.file = image_file
        super(Image, self).save(*args, **kwargs)


class VidMbed(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    video = EmbedVideoField()

    def getTitle(self):
        return self.name


class Podcast(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    pubdate = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    tags = models.CharField(max_length=256, blank=False, null=False)
    status = models.CharField(max_length=24, blank=False, null=False, choices=[('draft', 'drafting'), ('edit', 'editory'), ('publish', 'published')])
    recording = models.FileField(upload_to='podcasts')
    runtime = models.CharField(max_length=15, blank=False, null=False)
    filesize = models.IntegerField(default=0, blank=False, null=False)
    image = models.ForeignKey('Image')
    hitcount = models.IntegerField(default=0)
    sharedcount = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

    def updateHitCount(self):
        self.hitcount = self.hitcount + 1

    def updateSharedCount(self):
        self.sharedcount = self.sharedcount + 1

    def getTitle(self):
        return self.title
    
    class Meta:
        ordering = ['-pubdate']