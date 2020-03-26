from .views import FriendLinkView, BannerView, ActivityView
from django.urls import path


urlpatterns = [
    path('friendLink/', FriendLinkView.as_view()),
    path('banner/', BannerView.as_view()),
    path('activity/', ActivityView.as_view()),
]
