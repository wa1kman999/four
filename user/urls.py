from django.urls import path, re_path
from .views import LoginView,SmsLoginView, RegisterView, UserInfoView
from rest_framework.routers import DefaultRouter
from . import views
routers = DefaultRouter()
#我的课程
routers.register(r'myCourse', views.myCourseViewSet, basename='myCourse')
#通知的消息
routers.register(r'notification', views.NotificationViewSet, basename='notification')
#收藏列表
routers.register(r'favour', views.FavourViewSet, basename='favour')

#收藏课程
routers.register(r'favour1', views.Favour1ViewSet, basename='favour1')
#取消课程收藏,没搞出来
# routers.register(r'favour2', views.Favour2ViewSet, basename='favour2')

#评分
routers.register(r'rank', views.RankViewSet, basename='rank')
#我的课程
routers.register(r'myBought', views.MyCourseViewSet, basename='myBought')
#我的收益
routers.register(r'myearning', views.MyEarningViewSet, basename='myearning')





urlpatterns = [
    path('login/', LoginView.as_view()),  #普通登录
    path('smslogin/', SmsLoginView.as_view()),   #短信验证码登录
    path('register/', RegisterView.as_view()),  # 注册
    path('userinfo/', UserInfoView.as_view()),  # 注册
    re_path(r'^favour2/(?P<pk>\d+)/$', views.Favour2ViewSet.as_view()),

]
urlpatterns += routers.urls