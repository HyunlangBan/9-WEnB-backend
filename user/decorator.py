import jwt
import json
from django.http import jsonresponse
from user.models import user
from wenb.settings import SECRET_KEY, ALGORITHM

def login_check(func):
    def wrapper(self, request, *args, **kwargs):
        token = request.headers.get('authorization', none)
        if token is not none:
            try:
                decoded_token = jwt.decode(token, secret, algorithms = algorithm)
                user_id       = decoded_token['user_id']
                if user.objects.get(id=user_id):
                    user         = user.objects.get(id=user_id)
                    request.user = user
                    return func(self, request, *args, **kwargs)
            except jwt.decodeerror:
                return jsonresponse({'message': 'invalid_token'}, status = 400)
            except user.doesnotexist:
                return jsonresponse({'message': 'invalid_user'}, status = 400)
        return jsonresponse({'message': 'need_login'}, status = 401)
    return wrapper
