from django.db import models
from course.models import Course, Lecture


class User(models.Model):
    level_choice = (
        (0, '官方账号',),
        (1, '普通用户',)
    )
    password = models.CharField(max_length=256, editable=True, blank=True, null=True, verbose_name='用户密码')
    mobile = models.CharField(max_length=11, default='', blank=True, verbose_name='用户手机号')
    email = models.EmailField(default='', blank=True, verbose_name='用户邮箱')
    nick_name = models.CharField(max_length=32, default='', blank=True, verbose_name='昵称')
    region = models.CharField(max_length=255, default='', blank=True, verbose_name='地区')
    avatar_url = models.CharField(max_length=255, default='', blank=True, verbose_name='头像')
    open_id = models.CharField(max_length=255, default='', blank=True, verbose_name='微信open_id')
    union_id = models.CharField(max_length=255, default='', blank=True, verbose_name='微信union_id')
    gender = models.IntegerField(choices=((0, '未知'), (1, '男'), (2, '女')), default=0, verbose_name='性别')
    brief = models.CharField(max_length=32, default='这个人很懒...', verbose_name='个人一句话简介')
    desc = models.TextField(null=True, blank=True, verbose_name='个人介绍')
    level = models.IntegerField(choices=level_choice, default=1, verbose_name='账号等级')

    class Meta:
        db_table = 'f_user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nick_name

#优惠券
class PromotionBase(models.Model):
    promotion_classification_choice = (
        (1, '定额卷'),
        (2, '折扣卷'),
    )
    user = models.ForeignKey(to=User, null=True, blank=True, on_delete=models.CASCADE, related_name='promotion_base')
    classification = models.IntegerField(choices=promotion_classification_choice, verbose_name='优惠卷类型')
    value = models.DecimalField(null=True, max_digits=5, decimal_places=2, verbose_name='折扣值')
    brief = models.TextField(verbose_name='优惠卷使用说明')
    started = models.DateTimeField(null=True, blank=True, verbose_name='优惠开始')
    expire = models.DateTimeField(null=True, blank=True, verbose_name='过期时间')
    gen_count = models.IntegerField(null=True, blank=True, verbose_name='生成优惠卷数量')
    course = models.ManyToManyField(to=Course, related_name='promotion_base', verbose_name='使用范围')
    share = models.BooleanField(default=False, verbose_name='是否由分享获得')
    share_uuid = models.CharField(null=True, blank=True, max_length=32)

    def __str__(self):
        return self.brief

    class Meta:
        verbose_name = '优惠卷'

#优惠券码
class Promotion(models.Model):
    user = models.ForeignKey(to=User, null=True, on_delete=models.SET_NULL,
                             related_name='promotions', verbose_name='绑定用户')
    base = models.ForeignKey(to=PromotionBase, on_delete=models.CASCADE, related_name='gen_promotions')
    code = models.CharField(max_length=32, null=True, verbose_name='优惠码')
    status = models.BooleanField(default=False, verbose_name='是否使用')

    value = models.DecimalField(null=True, max_digits=5, decimal_places=2, verbose_name='折扣值')
    classification = models.IntegerField(default=1, verbose_name='优惠卷类型')
    started = models.DateTimeField(null=True, blank=True, verbose_name='优惠开始')
    expire = models.DateTimeField(null=True, blank=True, verbose_name='过期时间')
    brief = models.TextField(null=True, verbose_name='优惠卷使用说明')
    binding_time = models.DateTimeField(null=True, verbose_name='绑定时间')
    using_time = models.DateTimeField(null=True, verbose_name='使用时间')

    def __str__(self):
        return str(self.code)

    class Meta:
        verbose_name_plural = '优惠卷码'

#订单
class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='orders', verbose_name='用户')
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, null=True,
                               related_name='orders', verbose_name='课程')
    order_num = models.CharField(max_length=128, unique=True, null=True, verbose_name='订单号')
    final_price = models.DecimalField(null=True, max_digits=10, decimal_places=2, verbose_name='交易价格')
    start_time = models.DateTimeField(auto_now_add=True, verbose_name='交易开始时间')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='交易结束时间')
    pic = models.CharField(max_length=128, null=True, verbose_name='交易快照')
    paid = models.BooleanField(default=False, verbose_name='是否支付')

    def __str__(self):
        return self.order_num



#收益
class Earning(models.Model):
    target_choice = (
        ('course', '普通课程'),
        ('micro', '微课'),
        ('demo', 'Demo'),
    )
    approach_choice = (
        ('share', '分享收益'),
        ('sale', '销售收益'),
    )
    user = models.ForeignKey(to=User, related_name='earnings', on_delete=models.CASCADE)
    order = models.ForeignKey(to=Order, null=True, related_name='earnings', on_delete=models.SET_NULL)
    target = models.CharField(max_length=12, choices=target_choice, null=True)
    value = models.DecimalField(max_digits=6, decimal_places=2,)
    approach = models.CharField(max_length=32, choices=approach_choice)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def title(self):
        return self.order.course.title











 #提现记录
class WithdrawRecord(models.Model):
    record_status = (
        (0, '提现成功'),
        (1, '审核中'),
        (2, '提现失败'),
    )

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='withdraw', verbose_name='用户')
    alipay = models.CharField(max_length=32, null=True, verbose_name='支付宝账号')
    real_name = models.CharField(max_length=32, null=True, verbose_name='真实姓名')
    value = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='提现金额')
    status = models.IntegerField(choices=record_status, default=1, verbose_name='提现状态')
    created = models.DateTimeField(auto_now_add=True)

 # 收藏夹
class Favour(models.Model):  # 收藏夹
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='favour')
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, null=True,
                               related_name='favour', verbose_name='课程')

    def __str__(self):
        return str(self.user)

#历史课程
class HistoryCourse(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='history')
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, null=True,
                               related_name='history', verbose_name='课程')
    study_length = models.IntegerField(default=0, )
    study_time = models.DateTimeField(auto_now_add=True)

#历史课程列表
class HistoryLecture(models.Model):
    history_course = models.ForeignKey(to=HistoryCourse, on_delete=models.CASCADE, related_name='lectures')
    lecture = models.ForeignKey(to=Lecture, null=True, on_delete=models.CASCADE)
    study_length = models.IntegerField(default=0,)
    study_time = models.DateTimeField(auto_now_add=True)

#评论
class Comment(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='comments')
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, null=True,
                               related_name='comments', verbose_name='课程')
    content = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

#回复
class Reply(models.Model):
    user = models.ForeignKey(to=User, null=True, on_delete=models.CASCADE,)
    comment = models.ForeignKey(to=Comment, default='', on_delete=models.CASCADE, related_name='replies')
    reply_to = models.ForeignKey(to='Reply', null=True, on_delete=models.SET_NULL,
                                 related_name='replies')
    content = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    author = models.BooleanField(default=False)
    status = models.BooleanField(default=True)

#评分
class Rank(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='rank')
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, null=True,
                               related_name='rank', verbose_name='课程')
    rank = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='评分')
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

#通知
class Notification(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='notifications')
    from_user = models.ForeignKey(to=User, null=True, on_delete=models.SET_NULL, related_name='from_user')
    read = models.BooleanField(default=False)
    classification = models.CharField(max_length=32, verbose_name='通知类型')
    content = models.CharField(max_length=256, default='', verbose_name='通知内容')
    comment = models.CharField(max_length=256, default='', verbose_name='回复消息')
    url = models.CharField(max_length=256, verbose_name='跳转url')
    created = models.DateTimeField(auto_now_add=True)

#用户类型
class UserData(models.Model):
    level_choice = (
        (-1, '所有用户',),
        (0,  '官方账号',),
        (1,  '普通用户',)
    )
    user_classification = models.IntegerField(choices=level_choice, verbose_name='用户类型')

    class Meta:
        verbose_name = '用户数据'

    def __str__(self):
        return self.get_user_classification_display()

#销售数据
class SaleData(models.Model):
    course_classification_choice = (
        (0, '普通课程'),
        (1, '微课'),
        (2, 'Demo'),
        (3, '总量'),
    )
    course_classification = models.IntegerField(choices=course_classification_choice, verbose_name='课程类型')

    class Meta:
        verbose_name = '销售数据'

    def __str__(self):
        return self.get_course_classification_display()
