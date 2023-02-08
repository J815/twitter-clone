from django.shortcuts import render , redirect 
from django.http import HttpResponse, Http404 , JsonResponse
from django.conf import settings 

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Tweet 
from .forms import TweetForm 
from .serializers import TweetSerializer, TweetActionSerializer, TweetCreateSerializer

ALLOWED_HOSTS= settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request,"pages/feed.html")


def tweets_list_view(request, *args, **kwargs):
    return render(request,"tweets/list.html")

def tweet_detail_view(request, id, *args, **kwargs):
    return render(request,"tweets/detail.html", context={"id": id})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
   serializer= TweetSerializer(data= request.data)
   if serializer.is_valid(raise_exception= True):
       serializer.save(user=request.user)
       return Response(serializer.data, status= 201)
   return Response({}, status= 400)

def get_paginated_queryset_response(qs, request):
     paginator= PageNumberPagination()
     paginator.page_size= 20
     paginated_qs= paginator.paginate_queryset(qs, request)
     serializer= TweetSerializer(paginated_qs, many=True)
     return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tweet_feed_view(request, *args, **kwargs):
     user= request.user
     qs= Tweet.objects.feed(user)
     return get_paginated_queryset_response(qs, request)

@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
     qs= Tweet.objects.all()
     username= request.GET.get('username')
     if username != None:
        qs= qs.by_username(username)
     return get_paginated_queryset_response(qs, request)

@api_view(['GET'])
def details_view(request, tweet,*args,**kwargs):
     qs= Tweet.objects.filter(id= tweet)
     if not qs.exists():
       return Response({}, status= 404)
     obj= qs.first()
     serializer= TweetSerializer(obj)
     return Response(serializer.data, status=200)

@api_view(['DELETE','POST'])    
@permission_classes([IsAuthenticated])
def delete_view(request, tweet, *args, **kwargs):
     qs= Tweet.objects.filter(id= tweet)
     if not qs.exists():
       return Response({}, status= 404)
     qs=qs.filter(user= request.user)
     if not qs.exists():
       return Response({"message": "You can't delete this tweet"}, status= 401)
     obj= qs.first()
     obj.delete()
     return Response({"message":"Tweet removed"}, status= 200)

@api_view(['POST'])    
@permission_classes([IsAuthenticated])
def action_view(request, *args, **kwargs):
     serializer= TweetActionSerializer(data= request.data)
     if serializer.is_valid(raise_exception= True):
       data= serializer.validated_data
       id= data.get("id")
       action= data.get("action")
       content= data.get("content")
       qs= Tweet.objects.filter(id= id)
       if not qs.exists():
         return Response({}, status= 404)
       obj = qs.first()
       if action== "like":
         obj.likes.add(request.user)
         serializer= TweetSerializer(obj)
         return Response(serializer.data, status=200)
       elif action== "unlike":
         obj.likes.remove(request.user)
         serializer= TweetSerializer(obj)
         return Response(serializer.data, status=200)
       elif action== "retweet":
         new_tweet= Tweet.objects.create(user= request.user, parent= obj, content=content)
         serializer= TweetSerializer(new_tweet)
         return Response(serializer.data, status= 201)
     return Response({}, status=200)
     

def tweet_create_view_pure_django(request, *args , **kwargs):
   user= request.user 
   if not request.user.is_authenticated:
     user = None 
     if request.is_ajax():
       return JsonResponse({} , status= 401)
     return redirect(settings.LOGIN_URL)

   form= TweetForm(request.POST or None)
   homef_url= request.POST.get("next")

   if form.is_valid():
     formed= form.save(commit= False)
     formed.user= user 
     formed.save()
      
     if request.is_ajax():
       return JsonResponse(formed.serialize(), status= 201)
     if homef_url != None:
       return redirect(homef_url)
     form= TweetForm()
   if  form.errors:
      if request.is_ajax():
        return JsonResponse(form.errors , status=400)

   return render(request , "Parts/form.html",context={"form":form})

def details_view_pure_django(request, tweet,*args,**kwargs):
   try:
     obj= Tweet.objects.get(id=tweet)
   except:
     raise Http404
   data ={
      "id" : tweet,
      "content" : obj.content,
    }
   return JsonResponse(data)


def tweet_list_view_pure_django(request , *args, **kwargs):
   qs=Tweet.objects.all()
   tweet_list=[x.serialize() for x in qs ]

   data={
     "isUser": False,
     "response":tweet_list,
   }
   return JsonResponse(data)