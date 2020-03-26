from community import views
from django.urls import path, re_path,include

from rest_framework.routers import DefaultRouter
routers = DefaultRouter()
#文章详情
routers.register(r'article', views.ArticleViewSet, basename='article')
# #文章回复
# routers.register(r'reply', views.ReplyViewSet, basename='reply')
# routers.register(r'comment', views.ArticleCommentViewSet, basename='comment')
#文章点赞
routers.register(r'fav', views.ArticleFavViewSet, basename='fav')




urlpatterns = [
    path('', views.CommunityView.as_view()),
    path('classification/', views.ArticleClassificationView.as_view()),
    # path('article', views.ArticleView.as_view()),
    # path('article/', views.ArticleView.as_view()),  # 查看单个文章是就这么写
    # path('article/<int:pk>/', views.ArticleView.as_view()), #查看单个文章是就这么写
    # path('article/(\d+)/', views.ArticleView.as_view()),  # 查看单个数据是就这么写
    # re_path(r'^article/(?P<pk>\d+)/$', views.ArticleView.as_view()),

    # path('comment', views.Comment.as_view()),
    # path('reply', views.Reply.as_view()),
    # path('favour', views.Favour.as_view()),
    # path('', include(routers.urls))
    # path('comment', views.ArticleCommentView.as_view())
    re_path(r'^comment/(?P<pk>\d+)/$', views.ArticleCommentView.as_view()),


]

urlpatterns += routers.urls