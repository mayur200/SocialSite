from django.test import TestCase
from django.contrib.auth import get_user_model
from social_site.models import Tweet
from rest_framework.test import APIClient



User = get_user_model()

class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username = 'abc', password='abc_password')
        self.user2 = User.objects.create_user(username = 'user2', password='user_password')
        Tweet.objects.create(content="my tweset sec1", user=self.user)
        Tweet.objects.create(content="my t sweet 1sec1", user=self.user)
        Tweet.objects.create(content="my s tweet 2sec1", user=self.user)
        Tweet.objects.create(content="my sjk tweet 3sec1", user=self.user2)
        self.currentCount = Tweet.objects.all().count()

    def test_tweet_created(self):
        spirit_obj = Tweet.objects.create(content = 'my spirit sec2', user=self.user)
        self.assertEqual(spirit_obj.id,5)
        self.assertEqual(spirit_obj.user, self.user)

    # def test_user_created(self):
    #     user = User.objects.get(username = "abc")
    #     self.assertEqual(user.username, "abc")

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='abc_password')
        return client

    def test_tweet_list(self):
        client = self.get_client()
        response = client.get('/home/api/spirit/spirit/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()),4)
        print(response.json())

    def test_action_like(self):
        client = self.get_client()
        response = client.post('/home/api/spirit/action/', {"id":1,"action":"like"})
        self.assertEqual(response.status_code, 200)
        print(response.json())
        like_count = response.json().get('likes')
        self.assertEqual(like_count, 1)

    def test_action_unlike(self):
        client = self.get_client()
        response = client.post('/home/api/spirit/action/', {"id":2,"action":"like"})
        self.assertEqual(response.status_code, 200)
        response = client.post('/home/api/spirit/action/', {"id":2,"action":"unlike"})
        self.assertEqual(response.status_code, 200)
        print(response.json())
        like_count = response.json().get('likes')
        self.assertEqual(like_count, 0)

    def test_action_retweet(self):
        client =  self.get_client()
        current_count = self.currentCount
        response = client.post('/home/api/spirit/action/', {"id":2,"action":"re-spirit"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_tweet_id = data.get('id')
        self.assertNotEqual(2, new_tweet_id)
        self.assertEqual(current_count +1, new_tweet_id)


    def test_tweet_create_api_view(self):
        request_data = {'content':'This is my test tweet'}
        client = self.get_client()
        response = client.post("/home/api/spirit/cr_spirit/",request_data)
        self.assertEqual(response.status_code,201)
        response_data = response.json()
        new_tweet_id = response_data.get("id")
        self.assertEqual(self.currentCount +1, new_tweet_id)

    def test_tweet_detail_api_view(self):
        client = self.get_client()
        response = client.get('/home/api/spirit/1/')
        self.assertEqual(response.status_code,200)
        data = response.json()
        _id = data.get("id")
        self.assertEqual(_id, 1)

    def test_tweet_delete_api_view(self):
        client = self.get_client()
        response = client.delete('/home/api/spirit/1/delete/')
        self.assertEqual(response.status_code, 200)
        client = self.get_client()
        response = client.delete('/home/api/spirit/1/delete/')
        self.assertEqual(response.status_code, 404)
        response_incorrect_owner = client.delete('/home/api/spirit/4/delete/')
        self.assertEqual(response_incorrect_owner.status_code, 401)




