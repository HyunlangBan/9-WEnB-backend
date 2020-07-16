from django.urls import path
from user.views import KakaoSignInView, WishListView

urlpatterns = [
    path('/signin/kakao', KakaoSignInView.as_view()),
    path('/wishlist', WishListView.as_view()),
]
