# Create your views here.
from django.db import transaction
from django.template import RequestContext, loader
from django.http import HttpResponse, JsonResponse
from PIL import Image
from resizeimage import resizeimage
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from maynardlabs.forms import UserForm, ProfileForm
import json
import datetime
import csv            
import logging

logger = logging.getLogger(__name__)

from maynardlabs.utils import getLastThreeBlogs, getBlogByTitle, getLastThreePodcasts, getLastThreeVids, getAllBlogs, getAllPodcasts, getAllVids

def index(request):
    last_three_blogs = getLastThreeBlogs()
    logger.info("Last 3 Blogs returned: " + str([blog.getTitle() for blog in last_three_blogs]))
    last_three_podcasts = getLastThreePodcasts()
    logger.info("Last 3 podcasts returned: " + str([podcast.getTitle() for podcast in last_three_podcasts]))
    last_three_vids = getLastThreeVids()
    logger.info("Last 3 Vids returned: " + str([vid.getTitle() for vid in last_three_vids]))
    template = loader.get_template('index.html')
    context = RequestContext(request,
                             {'navbaractive': "home", 'blogs': last_three_blogs, 'podcasts': last_three_podcasts,
                              'videos': last_three_vids})
    return HttpResponse(template.render(context))


def blog(request):
    blogs = getAllBlogs()
    template = loader.get_template('index.html')
    context = RequestContext(request, {'navbaractive':"blogs", 'blogs':blogs})
    return HttpResponse(template.render(context))

def podcast(request):
    podcasts = getAllPodcasts()
    template = loader.get_template('index.html')
    context = RequestContext(request, {'navbaractive': "podcasts", 'podcasts':podcasts})
    return HttpResponse(template.render(context))

def vids(request):
    vids = getAllVids()
    template = loader.get_template('index.html')
    context = RequestContext(request, {'navbaractive': "vids", 'vids':vids})
    return HttpResponse(template.render(context))

@csrf_exempt
def blogview(request):
    body = json.loads(request.body)
    blogtitle = body.get('blogtitle', None)
    blog = getBlogByTitle(blogtitle)
    logger.debug("got request to display blog: " + blogtitle)
    template = loader.get_template('blogview.html')
    context = RequestContext(request, {'blog': blog})
    html = template.render(context)
    jsondict={}
    jsondict['htmlresponse'] = html
    return JsonResponse(jsondict)

@login_required(login_url='/members/login')
@transaction.atomic
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.Post, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = profile_form.cleaned_data.get('birth_date')
            user.profile.phone_number = profile_form.cleaned_data.get('phone_number')
            user.profile.bio = profile_form.cleaned_data.get('bio')
            user.profile.address = profile_form.cleaned_data.get('address')
            user.save()
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})