from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from Utils.utils import create_token
from user.models import User
from .serializers import LoginViewSerializer
from .serializers import MobileViewSerializer
from django.core.cache import cache
from Utils.AliMsg import SendSmsObject, create_code
from django.conf import settings
from .serializers import SmsLoginViewSerializer
from .serializers import RegisterViewSerializer
from .serializers import UserInfoViewSerializer
from rest_framework import mixins
from Utils.jwtAuth import JWTAuthentication
from . import serializers
from rest_framework import viewsets
from course.models import Course
from django_filters.rest_framework import DjangoFilterBackend
from course.filters import CourseFilter
from . import models
from Utils.visitThrottle import VisitThrottle


# # 用户nick_name和密码登录
class LoginView(generics.GenericAPIView):
    serializer_class = LoginViewSerializer
    '''登录接口'''

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response({'msg': '输入数据不合法', 'errorcode': 2, 'data': {}})
            data = serializer.data
            username = data.get('nick_name')
            password = data.get('password')
            print(data)
            print(username)
            print(password)
            user_obj = User.objects.filter(Q(mobile=username) | Q(email=username) | Q(nick_name=username)).first()
            if not user_obj:
                return Response({'msg': '用户不存在', 'errorcode': 2, 'data': {}})
            if user_obj.password == password:  # 要加密才能使用，不能再数据库中明文显示密码
                token_data = create_token({'id': user_obj.id})  # 生成一个token
                print(user_obj.id)
                return Response({'msg': '登录成功', 'errorcode': 0, 'data': token_data})
            else:
                return Response({'msg': '密码错误', 'errorcode': 2, 'data': {}})
        except Exception as e:
            print('发生错误：', e)
            return Response({'msg': '发生了错误', 'errorcode': 2, 'data': {}})


# 发送短信验证码
class MobileCodeView(generics.GenericAPIView):
    serializer_class = MobileViewSerializer

    def post(self, request):
        '''发送短信验证码接口'''
        try:
            json_data = {'msg': 'ok', 'errorCode': 0, 'data': {}}
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response({'msg': str(serializer.errors), 'errorCode': 2, 'data': {}})
            mobile = serializer.data.get('mobile')  # 获取手机号
            check_code = cache.get(mobile)  # 从redis缓存中检查是否获取了手机号
            if check_code:
                return Response({'msg': '验证码已经发送，请勿重复提交', 'errorCode': 2, 'data': {}})
            random_code = create_code()
            send_obj = SendSmsObject(settings.ALI_KEY, settings.ALI_SECRET, settings.ALI_REGION)
            return_msg = send_obj.send_code(settings.ALI_LOGOIN_CODE, mobile, random_code)
            if return_msg['Code'] != 'OK':
                json_data['message'] = '发送失败， 请更换手机号或重新尝试'
                json_data['errorCode'] = '2'
            # 设置缓存         此处还没安装redis  记得安装 并且再配置中配置
            cache.set(mobile, random_code, timeout=5 * 60)  # 缓存中key 为mobile，value为验证码
            return Response(json_data)
        except Exception as e:
            print('发生错误：', e)
            return Response({'msg': '出现了无法预料的视图错误', 'errorCode': 2, 'data': {}})


# 短信验证码登录
class SmsLoginView(generics.GenericAPIView):
    serializer_class = SmsLoginViewSerializer

    def post(self, request):
        # data = request.data
        # print(data)
        # phone = data.get('mobile')
        # print(phone)
        # return Response({'MSG':'HA'})
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response({'msg': str(serializer.errors), 'errorCode': 2, 'data': {}})
            data = serializer.data
            # return Response({'MSG': data})
            # print(data)
            phone = data.get('mobile')
            code = data.get('mobileCode')
            user_obj = User.objects.filter(mobile=phone).first()
            if not user_obj:
                return Response({'msg': '没有此用户名,请先注册', 'errorCode': 2, 'data': {}})
            if not cache.has_key(phone):
                return Response({'msg': '没有此手机号，请重新发送', 'errorCode': 2, 'data': {}})
            random_code = cache.get(phone)
            if code == random_code:
                token_data = create_token({'username': user_obj.id})  # 生成一个token
                return Response({'msg': '登陆成功', 'errorCode': 0, 'data': token_data})
            return Response({'msg': '输入验证码错误，请重新输入', 'errorCode': 2, 'data': {}})
        except Exception as e:
            print('发生错误：', e)
            return Response({'msg': '出现无法预料的视图错误', 'errorCode': 2, 'data': {}})


# 用户注册
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterViewSerializer

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response({'msg': str(serializer.errors), 'errorCode': 2, 'data': {}})
            serializer.save()
            # data = serializer.data
            # print(data)
            # nick_name = data.get('nick_name')
            # mobile = data.get('mobile')
            # email = data.get('email')
            # password = data.get('password')
            # user_obj = User.objects.filter(Q(nick_name=nick_name) | Q(mobile=mobile) | Q(email=email)).first()
            # if user_obj:
            #     return Response({'msg': '该用户已经注册', 'errorCode': 2, 'data': {}})
            # User.objects.create(nick_name=nick_name, mobile=mobile, email=email, password=password)
            return Response({'msg': '恭喜你注册成功', 'errorCode': 0, 'data': {}})
        except Exception as e:
            print('发生错误：', e)
            return Response({'msg': '发生视图错误', 'errorCode': 2, 'data': {}})


# 获取和修改个人信息
# 个人信息
class UserInfoView(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserInfoViewSerializer
    authentication_classes = (JWTAuthentication, )

    def get_queryset(self):
        print(list(models.User.objects.filter(id=self.request.user.id)))
        return list(models.User.objects.filter(id=self.request.user.id))

    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user, data=request.data, partial=False)   #这个是个人用户信息更新
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# 修改密码

class ChangePwdView(mixins.CreateModelMixin, generics.GenericAPIView):
    authentication_classes = (JWTAuthentication,)
    serializer_class = serializers.PasswordSerializer


# 我上传的课程
class myCourseViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JWTAuthentication,)
    serializer_class = serializers.myCourseViewSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = CourseFilter  # 记得在APP中注册filter

    def get_queryset(self):
        return Course.objects.filter(user=self.request.user.id)


# 获取通知消息和标记为已读


class NotificationViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JWTAuthentication,)
    serializer_class = serializers.NotificationViewSerializer

    def get_queryset(self):
        user_obj = self.request.user
        print(user_obj)
        print(user_obj.id)
        # notification = user_obj.notifications.order_by('-created')
        notification = models.Notification.objects.filter(user=user_obj.id).order_by('-created')
        if notification:
            notification = notification.filter(classification=self.request.query_params.get('classification'))
            print(notification)
            return notification


# 收藏课程列表
class FavourViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JWTAuthentication, )
    throttle_classes = (VisitThrottle, )
    serializer_class = serializers.FavourViewSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = CourseFilter

    def get_queryset(self):
        print(self.request.user)
        return Course.objects.filter(user=self.request.user.id)


# 收藏课程
class Favour1ViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JWTAuthentication,)
    serializer_class = serializers.FavourView1Serializer
    lookup_field = 'course'   #对应的就是url上的参数

    def get_queryset(self):
        return models.Favour.objects.filter(user=self.request.user.id)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


# 评分
class RankViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JWTAuthentication,)
    serializer_class = serializers.RankViewSerializer
    queryset = models.Rank.objects.all()


# 我的课程
class MyCourseViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JWTAuthentication,)
    serializer_class = serializers.MyBoughtViewSerializer

    def get_queryset(self):
        user_obj = self.request.user
        order = user_obj.orders.filter(paid=True)  # 得到这个人所有的订单
        # myBought = order.filter(course__user=user_obj.id)
        print(order)
        return order
        # order_obj = models.Order.objects.get(user=user_obj)
        # print(order_obj)
        # print(str(order_obj.course.id))
        # return str(order_obj.course.id)


# 我的收益
class MyEarningViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JWTAuthentication,)
    serializer_class = serializers.MyEarningViewSerializer

    def get_queryset(self):
        user_obj = self.request.user
        earn_obj = models.Earning.objects.filter(user=user_obj)
        return earn_obj
