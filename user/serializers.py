from rest_framework import serializers
import re
from Utils.utils import is_safe_password
from user.models import User
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.validators import UniqueTogetherValidator
from course.models import Course
from . import models


# 登录
class LoginViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nick_name', 'password']


# 发送短信
class MobileViewSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = User
    #     fields = ['mobile']
    mobile = serializers.CharField()


# 手机验证码登录
class SmsLoginViewSerializer(serializers.Serializer):
    # class Meta:
    #     model = User
    #     fields = ['mobile']
    mobile = serializers.CharField(max_length=11, )

    def validate_mobile(self, mobile):
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        # if User.objects.filter(mobile=mobile).count():
        #     raise serializers.ValidationError("用户已经存在")
        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")
        return mobile
        #     # 验证码发送频率
        # one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        # if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
        #     raise serializers.ValidationError("距离上一次发送未超过60s")

    # def to_representation(self, instance):
    #     students_dict = super().to_representation(instance)  # 调用父类的to_representation方法，将对象拆分为字典对象
    #     student_dict["position"] = "共青团员"  # 给学生添加position的新属性
    #     return student_dict
    # def validate(self, attrs):
    #     mobileCode = self.context['request'].data.get('mobileCode')
    #     print(self.context['request'])
    #     print(mobileCode)
    #     print(attrs)
    #     # if len(mobileCode) != 6:
    #     #     raise serializers.ValidationError('输入的验证码长度不对')
    #     return attrs, mobileCode
    mobileCode = serializers.CharField()

    def validate_mobileCode(self, mobileCode):  # 新定义的关于手机验证码的字段
        if len(mobileCode) != 6:
            raise serializers.ValidationError('输入的验证码长度不对，请重新输入')
        return mobileCode


# 用户注册
class RegisterViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mobile', 'email', 'nick_name', 'password']
        validators = [
            UniqueTogetherValidator(queryset=User.objects.all(), fields=['mobile', ], message='此手机号已经被注册'),
            UniqueTogetherValidator(queryset=User.objects.all(), fields=['email', ], message='此邮箱已经被注册'),
            UniqueTogetherValidator(queryset=User.objects.all(), fields=['nick_name', ], message='此用户名已经被注册'),
        ]

    def validate(self, attrs):
        print('attrs:', attrs)
        print('request1:', self.context['request'].user)
        print('request2:', self.context['request'].user)
        print('request3:', self.context['request'].data)
        print('request4:', self.context['request'].query_params)
        print('view:', self.context['view'].kwargs)

        return attrs


# 修改个人信息
class UserInfoViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nick_name', 'region', 'avatar_url', 'gender', 'brief', 'desc']




# 修改密码
class PasswordSerializer(serializers.Serializer):
    """
    修改密码
    """
    old_password = serializers.CharField(label="旧密码", help_text="旧密码", required=True,
                                         style={'input_type': 'password'}, trim_whitespace=False)
    password = serializers.CharField(label='新密码', help_text="新密码", required=True,
                                     style={'input_type': 'password'}, trim_whitespace=False)
    confirm_password = serializers.CharField(label='确认密码', help_text="确认密码", required=True,
                                             style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("二次密码不相同")
        if password == old_password:
            raise serializers.ValidationError("新密码和旧密码相同")
        if not is_safe_password(password):
            raise serializers.ValidationError("密码安全强度不符合，密码要求包含大小写字母和数字,密码长度至少8位")
        del old_password
        del confirm_password
        return attrs


# 我上传的课程
class myCourseViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


# 通知消息

class NotificationViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = "__all__"

    not_read = serializers.SerializerMethodField()

    def get_not_read(self, obj):
        res = models.Notification.objects.filter(read=False).count()
        return res


# 收藏相关
class FavourViewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Course
        fields = "__all__"


# 收藏课程
class FavourView1Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Favour
        fields = ['course', ]

    def validate(self, attrs):
        user_obj = self.context['request'].user
        attrs['user'] = user_obj
        f = models.Favour.objects.filter(user=user_obj, course=attrs['course'])
        # print(f)
        if f:
            raise serializers.ValidationError('已经收藏1111111')
        return attrs


# 取消课程收藏
# class FavourView2Serializer(serializers.ModelSerializer):
#     # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     class Meta:
#         model = models.Favour
#         fields = ['course']

#
# def validate(self, attrs):
#     #     user_obj = self.context['request'].user
#     #     attrs['user'] = user_obj
#     #     # f = models.Favour.objects.filter(user=user_obj, course=attrs['course'])
#     #     # if not f:
#     #     #     raise serializers.ValidationError('请先收藏')
#     #     return attrs


# 评分
class RankViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rank
        fields = ['course', 'rank', ]

    def validate(self, attrs):
        user_obj = self.context['request'].user
        attrs['user'] = user_obj
        return attrs


# 我的课程
class MyBoughtViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ['id']


# 我的收益
class MyEarningViewSerializer(serializers.ModelSerializer):
    all_earning = serializers.SerializerMethodField()
    approach = serializers.CharField(source='get_approach_display')

    class Meta:
        model = models.Earning
        fields = ['all_earning', 'title', 'approach', 'value', 'created']

    def get_all_earning(self, obj):
        all_earning = 0
        user_obj = self.context['request'].user
        earnings = user_obj.earnings.order_by('-created')
        print(earnings)
        for i in earnings:
            all_earning += i.value
        return all_earning
