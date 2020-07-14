from django.urls import path
from user.views import KakaoSignInView, KakaoSignUpView

urlpatterns = [
    path('/signin/kakao', KakaoSignInView.as_view()),
]
