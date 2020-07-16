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

class WishListTest(TestCase):
    def setUp(self):
        Tag.objects.create(id=1, title="Title1", detail="detail1")
        Host.objects.create(id=1, description="Host1", is_superhost=False)
        BuildingType.objects.create(id=1, name="type1")
        HouseType.objects.create(id=1, name="house1")
        BuildingHouseType.objects.create(
                id            = 1,
                building_type = BuildingType.objects.get(id = 1),
                house_type    = HouseType.objects.get(id = 1)
                )
        User.objects.create(
                id              = 1,
                nickname        = 'test_user',
                thumbnail_image = 'https://interactive-examples.mdn.mozilla.net/media/examples/grapefruit-slice-332-332.jpg',
                is_host         = False,
                email           = 'test@email.com',
                kakao_id        = 12345
                )
        Stay.objects.create(
                id             = 1,
                title          = "소길숲속 효리네 민박 옆집",
                address        = '애월읍, 제주시, 제주도, 한국',
                sub_title      = '건용님이 호스팅하는 타운하우스의 개인실',
                price          = 60000.00,
                capacity       = 2,
                bedroom_count  = 1,
                bathroom_count = 1,
                longitude      = 126.373900,
                latitude       = 33.430870,
                tag            = Tag.objects.get(id = 1),
                host           = Host.objects.get(id = 1),
                building_house = BuildingHouseType(id = 1)
                )

    def tearDown(self):
        User.objects.all().delete()
        Stay.objects.all().delete()

    def test_wishlist_post_success(self):
        client   = Client()
        header   = {'HTTP_AUTHORIZATION': token}
        response = client.post('/user/wishlist', json.dumps({'stay_id': 1}), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_wishlist_post_invalid_key(self):
        client   = Client()
        header   = {'HTTP_AUTHORIZATION': token}
        response = client.post('/user/wishlist', json.dumps({'stay': 1}), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_wishlist_post_404_error(self):
        client   = Client()
        header   = {'HTTP_AUTHORIZATION': token}
        response = client.post('/user/wish_list', json.dumps({'stay_id': 1}), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 404)

    def test_wishlist_get_success(self):
        client   = Client()
        header   = {'HTTP_AUTHORIZATION': token}
        response = client.get('/user/wishlist', **header)
        self.assertEqual(response.status_code, 200)

    def test_wishlist_get_404_error(self):
        client   = Client()
        header   = {'HTTP_AUTHORIZATION': token}
        response = client.get('/user/wish_list', **header)
        self.assertEqual(response.status_code, 404)
