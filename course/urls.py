from course import views
from django.urls import path, re_path, include

from rest_framework.routers import DefaultRouter
routers = DefaultRouter()
#课程信息
routers.register(r'courseInfo', views.CourseInfoViewSet, basename='courseInfo')
#课程详情
routers.register(r'courseDetail', views.CourseDetailViewSet, basename='courseDetail')
#课程标签
routers.register(r'courseTag', views.CourseTagViewSet, basename='courseTga')
#课程目录
routers.register(r'courseCatalogue', views.CourseCatalogueViewSet, basename='courseCatalogue')
#课程视频连接
routers.register(r'courseVideo', views.CourseVideoViewSet, basename='courseVideo')




urlpatterns = [

]

urlpatterns += routers.urls