from django.test import TestCase
from django.contrib.auth import get_user_model
# Create your tests here.
from rest_framework.test import APIClient
from .models import Profile
User= get_user_model()

class ProfileTestCase(TestCase):
    def setUp(self):
        self.usera= User.objects.create_user(username='juba',password='123tyuopkj')
        self.userb= User.objects.create_user(username='kamau',password='123tyuoplj')

    def get_client(self):
        client= APIClient()
        client.login(username=self.usera.username, password='123tyuopkj')
        return client

    def test_profile_created_via_signal(self):
        qs= Profile.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_following(self):
        first= self.usera
        second= self.userb
        first.profile.followers.add(second)
        second_user_following_whom= second.following.all()
        qs= second_user_following_whom.filter(user=first)
        first_user_following_no_one= first.following.all()
        self.assertTrue(qs.exists())
        self.assertFalse(first_user_following_no_one.exists())

    def test_follow_api_endpoint(self):
        client=self.get_client()
        response= client.post(f"/api/profiles/{self.userb.username}/follow", {"action": "follow"})
        res_data= response.json()
        counting= res_data.get("count")
        self.assertEqual(counting, 1)

    def test_unfollow_api_endpoint(self):
        first= self.usera
        second= self.userb
        first.profile.followers.add(second)
        client=self.get_client()
        response= client.post(f"/api/profiles/{self.userb.username}/follow", {"action": "unfollow"})
        res_data= response.json()
        counting= res_data.get("count")
        self.assertEqual(counting, 0)

    def test_cannot_follow_api_endpoint(self):
        client=self.get_client()
        response= client.post(f"/api/profiles/{self.usera.username}/follow", {"action": "follow"})
        res_data= response.json()
        counting= res_data.get("count")
        self.assertEqual(counting, 0)