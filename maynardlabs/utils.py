from django.core.exceptions import ObjectDoesNotExist
from maynardlabs.models import Blog, Podcast, VidMbed

#Blog Data Access utility methods
def getLastThreeBlogs():
    return Blog.objects.all()[:3]

def getAllBlogs():
    return Blog.objects.all()

def getBlogByTitle(title):
    return Blog.objects.get(title__iexact=title)

def getBlogById(id):
    return Blog.objects.get(pk=id)

#Podcast Data Access Utility Methods
def getAllPodcasts():
    return Podcast.objects.all()

def getLastThreePodcasts():
    return Podcast.objects.all()[:3]

def getPodcastByTitle(title):
    return Podcast.objects.get(title__iexact=title)

def getPodcastById(id):
    return Blog.objects.get(pk=id)

#Video Data Access Utility Methods
def getAllVids():
    return VidMbed.objects.all()

def getLastThreeVids():
    return VidMbed.objects.all()[:3]

def getVidByTitle(title):
    return VidMbed.objects.get(title__iexact=title)

def getVidById(id):
    return VidMbed.objects.get(pk=id)