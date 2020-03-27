from django.urls import path, re_path
from .views import LoginView, SmsLoginView, RegisterView, UserInfoView, ChangePwdView
from rest_framework.routers import DefaultRouter
from . import views
routers = DefaultRouter()

#个人的用户信息
routers.register(r'myinfo', views.UserInfoView, basename='myinfo')
#我的课程
routers.register(r'myCourse', views.myCourseViewSet, basename='myCourse')
#通知的消息
routers.register(r'notification', views.NotificationViewSet, basename='notification')
#收藏列表
routers.register(r'favour', views.FavourViewSet, basename='favour')
#收藏课程
routers.register(r'favour1', views.Favour1ViewSet, basename='favour')
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
    path('changepwd/', ChangePwdView.as_view()),  #修改密码


]
urlpatterns += routers.urls