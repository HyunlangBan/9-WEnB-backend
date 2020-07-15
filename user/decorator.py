import jwt
import json

from django.http   import JsonResponse

from user.models   import User
from wenb.settings import SECRET_KEY, ALGORITHM

def login_check(func):
    def wrapper(self, request, *args, **kwargs):
        token = request.headers.get('authorization', None)
        if token:
            try:
                decoded_token = jwt.decode(token, SECRET_KEY, algorithms = ALGORITHM)
                user_id       = decoded_token['user_id']
                if User.objects.filter(id=user_id).exists():
                    request.user = User.objects.get(id=user_id)
                    return func(self, request, *args, **kwargs)
            except jwt.DecodeError:
                return JsonResponse({'message': 'invalid_token'}, status = 400)
            except User.DoesNotExist:
                return JsonResponse({'message': 'invalid_user'}, status = 400)
        return JsonResponse({'message': 'need_login'}, status = 401)
    return wrapper
