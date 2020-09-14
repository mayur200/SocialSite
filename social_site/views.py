from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from .models import Tweet

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request,"pages/home.html", context={})

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
    tweet_list = [{'id':x.id,'content':x.content}for x in qs]
    data = {
        "isUser": False,
        'response': tweet_list
    }
    return JsonResponse(data)




