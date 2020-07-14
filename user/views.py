import json
import jwt
import requests
from django.views  import View
from user.models   import User
from django.http   import JsonResponse
from wenb.settings import SECRET_KEY, ALGORITHM

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
