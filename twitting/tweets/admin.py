from django.contrib import admin

# Register your models here.
from .models import Tweet, UserLike

class UserLikeAdmin(admin.TabularInline):
    model= UserLike

class TweetAdmin(admin.ModelAdmin):
    inlines= [UserLikeAdmin]
    list_display= ['__str__', 'user']
    class Meta:
        model= Tweet

admin.site.register(Tweet, TweetAdmin)