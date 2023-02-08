from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient
from .models import Tweet
# Create your tests here.
User= get_user_model()


class TweetTestCase(TestCase):
    def setUp(self):
        self.usera= User.objects.create_user(username='juba',password='123tyuopkj')
        self.userb= User.objects.create_user(username='kamau',password='123tyuoplj')
        Tweet.objects.create(content="first tweet", user= self.usera)
        Tweet.objects.create(content="first tweet", user= self.usera)
        Tweet.objects.create(content="first tweet", user= self.userb)
        Tweet.objects.create(content="first tweet", user= self.userb)
        self.currentCount= Tweet.objects.all().count()

    def test_tweet_created(self):
        obj= Tweet.objects.create(content="second tweet", user=self.usera)
        self.assertEqual(obj.id, 5)
        self.assertEqual(obj.user, self.usera)

    def get_client(self):
        client= APIClient()
        client.login(username= self.usera.username, password='123tyuopkj')
        return client

    def test_tweet_list(self):
        client= self.get_client()
        response= client.get("/api/twe/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)

    def test_tweets_related_name(self):
        user= self.usera
        self.assertEqual(user.tweets.count(), 2)

    def test_action_like(self):
        client= self.get_client()
        response= client.post("/api/twe/action", {"id":1, "action":"like"})
        like_c= response.json().get("likes")
        user= self.usera
        like_instances_count= user.userlike_set.count()
        related_likes= user.user_like.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(like_c, 1)
        self.assertEqual(like_instances_count, 1)
        self.assertEqual(like_instances_count, related_likes)

    def test_action_unlike(self):
        client= self.get_client()
        response= client.post("/api/twe/action", {"id":2, "action":"like"})
        self.assertEqual(response.status_code, 200)
        response= client.post("/api/twe/action", {"id":2, "action":"unlike"})
        self.assertEqual(response.status_code, 200)
        like_c= response.json().get("likes")
        self.assertEqual(like_c, 0)

    def test_action_retweet(self):
        client= self.get_client()
        response= client.post("/api/twe/action", {"id":3, "action":"retweet"})
        self.assertEqual(response.status_code, 201)
        data= response.json()
        retweet_id= data.get("id")
        self.assertNotEqual(retweet_id, 3)
        self.assertEqual(retweet_id, self.currentCount + 1)

    def test_tweet_create_api_view(self):
        request_data= {"content":"this is third data"}
        client= self.get_client()
        response= client.post("/api/twe/create", request_data)
        self.assertEqual(response.status_code, 201)
        response_data= response.json()
        new_id= response_data.get("id")
        self.assertEqual(new_id, self.currentCount + 1)
 
    def test_tweet_details_api_view(self):
        client= self.get_client()
        response= client.get("/api/twe/1/")
        self.assertEqual(response.status_code, 200)
        data= response.json()
        one_id= data.get("id")
        self.assertEqual(one_id, 1)

    def test_tweet_delete_api_view(self):
        client= self.get_client()
        response= client.delete("/api/twe/1/delete")
        self.assertEqual(response.status_code, 200)
        client= self.get_client()
        response= client.delete("/api/twe/1/delete")
        self.assertEqual(response.status_code, 404)
        response_unauthorized= client.delete("/api/twe/4/delete")
        self.assertEqual(response_unauthorized.status_code, 401)
        
        