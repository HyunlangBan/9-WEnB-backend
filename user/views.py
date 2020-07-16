import json
import jwt
import requests
from functools      import reduce
from django.views   import View
from user.models    import User
from django.http    import JsonResponse
from django.db      import IntegrityError
from user.decorator import login_check
from stay.models    import Stay
from user.models    import WishList
from wenb.settings  import SECRET_KEY, ALGORITHM

class KakaoSignInView(View):
    def get(self, request):
        try:
            access_token    = request.headers.get('Authorization', None)
            uri             = 'https://kapi.kakao.com/v2/user/me'
            header          = {'Authorization': f'Bearer {access_token}'}
            profile_request = requests.get(uri, headers = header)
            profile_json    = profile_request.json()

            kakao_id        = profile_json['id']
            nickname        = profile_json['properties']['nickname']
            thumbnail_image = profile_json['properties'].get('thumbnail_image', None)
            email           = profile_json['kakao_account'].get('email', None)
        except KeyError:
            return JsonResponse( {'message': 'INVALID_KEYS'}, status = 400 )
        user, created = User.objects.get_or_create(nickname = nickname, email = email, thumbnail_image = thumbnail_image, is_host=False, kakao_id = kakao_id)
        token = jwt.encode({'user_id': user.id}, SECRET_KEY, algorithm = ALGORITHM).decode('utf-8')
        return JsonResponse( {'message': 'SUCCESS', 'token': token}, status = 200 )

class WishListView(View):
    @login_check
    def post(self, request):
        try:
            res     = json.loads(request.body)
            stay_id = res['stay_id']
            user    = request.user
            stay    = Stay.objects.get(id = stay_id)
            name    = stay.address.split(',')[-2]
            WishList.objects.create(user = user, stay = stay, name= name)
            return JsonResponse( {'message': 'SUCCESS'}, status = 200 )
        except KeyError:
            return JsonResponse( {'message': 'INAVLID_KEYS'}, status = 400)
        except IntegrityError:
            return JsonResponse( {'message': 'DUPLICATED_WISHITEM'}, status = 400 )

    @login_check
    def get(self, request):
        user              = request.user
        wishlists_objects = WishList.objects.filter(user = user)
        wishlists         = [
            {
                'title': wishlist.stay.title,
                'image': wishlist.stay.image_set.first().image_link,
                'address': reduce(lambda x,y: x+y, wishlist.stay.address.split(',')[:2])
            } for wishlist in wishlists_objects ]
        return JsonResponse( { 'wishlist': wishlists }, status = 200 ) 
