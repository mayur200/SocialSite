from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.conf import  settings
from django.utils.http import is_safe_url
from .models import Tweet
from .forms import SpiritForm
from .serializers import TweetSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect, get_object_or_404


import random

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request,"pages/home.html", context={})


@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def spirit_create_view(request, *args, **kwargs):
    serializer = TweetSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return  Response(serializer.data, status=201)
    return Response({},status=400 )

@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    '''
    REST API view consume by java/SWIFT/Android/iOS
    Return json data
    '''
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True) #qs = query set many=True (many object)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def tweet_detail_view(request,spirit_id, *args, **kwargs):
    '''
       REST API view consume by java/SWIFT/Android/iOS
       Return json data
    '''
    qs = Tweet.objects.filter(id=spirit_id)
    if not qs.exists():
        return Response({},status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(['DELETE','POST'])
def tweet_delete_view(request,spirit_id, *args, **kwargs):
    '''
       REST API view consume by java/SWIFT/Android/iOS
       Return json data
    '''
    qs = Tweet.objects.filter(id=spirit_id)
    if not qs.exists():
        return Response({},status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"Message":"You cannot delete this tweet"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message":"Tweet Removed"}, status=200)

def spirit_create_view_pure_django(request, *args, **kwargs):
    print("Request",request.is_ajax())
    user = request.user
    if not request.user.is_authenticated:
        user =  None
        if request.is_ajax():
            return  JsonResponse({},status=401)
        return redirect(settings.LOGIN_URL)
    form = SpiritForm(request.POST or None)
    nex_url = request.POST.get("next") or None
    print("next>>>>>>>>", nex_url)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(),status=201)
        # if nex_url != None and is_safe_url(nex_url,ALLOWED_HOSTS): #this will check if next_url is in the allowed hosts then only it will redirect otheriwse it will be render
        if nex_url != None and is_safe_url(nex_url): #this will check if next_url is in the allowed hosts then only it will redirect otheriwse it will be render
            return redirect(nex_url)
        form = SpiritForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'pages/form.html', context={"form":form})

def tweet_detail_view_pure_django(request,tweet_id, *args, **kwargs):
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

def tweet_list_view_pure_django(request, *args, **kwargs):
    '''
    REST API view consume by java/SWIFT/Android/iOS
    Return json data
    '''
    qs = Tweet.objects.all()
    tweet_list = [x.serialize()for x in qs]
    data = {
        "isUser": False,
        'response': tweet_list
    }
    return JsonResponse(data)




