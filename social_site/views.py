from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.conf import  settings
from django.utils.http import is_safe_url
from .models import Tweet
from .forms import SpiritForm
import random
ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request,"pages/home.html", context={})

def spirit_create_view(request, *args, **kwargs):
    print("Request",request.is_ajax())
    form = SpiritForm(request.POST or None)
    nex_url = request.POST.get("next") or None
    print("next>>>>>>>>", nex_url)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if request.is_ajax():
            return JsonResponse({},status=201)
        if nex_url != None and is_safe_url(nex_url,ALLOWED_HOSTS): #this will check if next_url is in the allowed hosts then only it will redirect otheriwse it will be render
            return redirect(nex_url)
        form = SpiritForm()
    return render(request, 'pages/form.html', context={"form":form})

def tweet_detail_view(request,tweet_id, *args, **kwargs):
    '''
       REST API view consume by java/SWIFT/Android/iOS
       Return json data
    '''
    data = {
        'id': tweet_id,
    }
    status = 202
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not Found"
        status = 404
    return JsonResponse(data, status)

def tweet_list_view(request, *args, **kwargs):
    '''
    REST API view consume by java/SWIFT/Android/iOS
    Return json data
    '''
    qs = Tweet.objects.all()
    tweet_list = [{'id':x.id,'content':x.content, 'likes':random.randint(0, 12)}for x in qs]
    data = {
        "isUser": False,
        'response': tweet_list
    }
    return JsonResponse(data)




