"""four URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPICodec
from rest_framework.documentation import include_docs_urls   #自动生成api文档

schema_view = get_schema_view(title='API', renderer_classes=[SwaggerUIRenderer, OpenAPICodec])


from course import views

from rest_framework.routers import DefaultRouter
routers = DefaultRouter()
#搜索的路由
routers.register(r'search', views.CourseSearchViewSet, basename='search')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('banner/', include('banner.urls')),
    path('community/', include('community.urls')),
    path('course/', include('course.urls')),
    # path(r'docs/', schema_view, name='docs')
    path("api-docs/", include_docs_urls("API文档")),
    path('', include('social_django.urls', namespace='social')),     #第三方登录的url
]

urlpatterns += routers.urls