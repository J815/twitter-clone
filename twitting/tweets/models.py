import random
from django.db import models
from django.conf import settings 
from django.db.models import Q
# Create your models here.
User= settings.AUTH_USER_MODEL 

class UserLike(models.Model):
    user= models.ForeignKey(User, on_delete= models.CASCADE)
    tweet= models.ForeignKey("Tweet", on_delete= models.CASCADE)
    time= models.DateTimeField(auto_now_add=True)

class TweetQuerySet(models.QuerySet):
    def by_username(self, username):
        return self.filter(user__username__iexact=username)

    def feed(self, user):
        profiles_exist= user.following.exists()
        followed_user_id=[]
        if profiles_exist:
            followed_user_id= user.following.values_list("user__id", flat=True)
        return self.filter(
            Q(user__id__in=followed_user_id) | Q(user=user)
        ).distinct().order_by("-time")

class TweetManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return TweetQuerySet(self.model, using=self._db)

    def feed(self, user):
        return self.get_queryset().feed(user)
    
class Tweet(models.Model):
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    user= models.ForeignKey(User , on_delete= models.CASCADE, related_name="tweets")
    likes= models.ManyToManyField(User, related_name='user_like', blank=True, through= UserLike)
    content=models.TextField(null=True,blank=True)
    img= models.FileField(upload_to='images/',null=True,blank=True)
    time= models.DateTimeField(auto_now_add=True)

    objects= TweetManager()

    class Meta:
        ordering =['-id']

    def retweet(self):
        return  self.parent != None

    def serialize(self):
       return { 
        "id" : self.id ,
        "content" : self.content,
        "likes" : random.randint(0, 100)
       }