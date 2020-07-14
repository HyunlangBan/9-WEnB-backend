import json
from django.test import TestCase
from django.test import Client
from unittest.mock import patch
from user.models import User

class KakaoSignInTest(TestCase):
    def setUp(self):
        User.objects.create(id=1, nickname = 'test_user', thumbnail_image = 'https://interactive-examples.mdn.mozilla.net/media/examples/grapefruit-slice-332-332.jpg', is_host = False, email = 'test@email.com', kakao_id = 12345)

    def tearDown(self):
        User.objects.all().delete()

    def test_kakao_signin_success(self):
        with patch('user.views.requests.get') as mocked_get:

            class UserInfo:
                def json(self):
                    user_info  = {
                        'id': 12345,
                        'properties': {'nickname': 'test_user', 'thumbnail_image': 'https://interactive-examples.mdn.mozilla.net/media/examples/grapefruit-slice-332-332.jpg'},
                        'kakao_account': {'email': 'test@email.com'}
                    }
                    return user_info

            user_profile = UserInfo()
            mocked_get.return_value = user_profile 
            
            client = Client()
            response = client.get('/user/signin/kakao')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.json()['token'])

    def test_kakao_signin_new_user(self):
        with patch('user.views.requests.get') as mocked_get:

            class UserInfo:
                def json(self):
                    user_info  = {
                        'id': 678910,
                        'properties': {'nickname': 'new_user', 'thumbnail_image': 'https://interactive-examples.mdn.mozilla.net/media/examples/grapefruit-slice-332-332.jpg'},
                        'kakao_account': {'email': 'new_user@email.com'}
                    }
                    return user_info

            user_profile = UserInfo()
            mocked_get.return_value = user_profile 

            client = Client()
            response = client.get('/user/signin/kakao')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.json()['token'])

    def test_kakao_signin_404_error(self):
        with patch('user.views.requests.get') as mocked_get:

            class UserInfo:
                def json(self):
                    user_info  = {
                        'kakao-id': 12345,
                        'properties': {'nickname': 'test_user', 'thumbnail_image': 'https://interactive-examples.mdn.mozilla.net/media/examples/grapefruit-slice-332-332.jpg'},
                        'kakao_account': {'email': 'test@email.com'}
                    }
                    return user_info

            user_profile = UserInfo()
            mocked_get.return_value = user_profile 
            
            client = Client()
            response = client.get('/user/signin')
            self.assertEqual(response.status_code, 404)
