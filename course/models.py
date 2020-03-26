from django.db import models
from django.utils.deconstruct import deconstructible
# from mdeditor.fields import MDTextField
from uuid import uuid4




@deconstructible
class UploadTo(object):
    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid4().hex, ext)
        return self.sub_path + filename

#标签
class Tag(models.Model):
    content = models.CharField(max_length=64, verbose_name='标签')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = '标签'

#课程信息
class Course(models.Model):
    target_choice = (
        ('course', '课程'),
        ('micro', '微课'),
        ('demo', 'Demo'),
    )
    target = models.CharField(choices=target_choice, default='course', max_length=12, verbose_name='课程类型')
    user = models.IntegerField(verbose_name='上传用户ID')
    title = models.CharField(max_length=128, blank=False, null=True, verbose_name='标题')
    brief = models.TextField(default='', verbose_name='课程简介')
    desc = models.TextField(blank=True, null=True, verbose_name='课程介绍')
    thumbnail = models.CharField(max_length=256, null=True, blank=True, verbose_name='课程图')
    is_video = models.BooleanField(default=True, null=True, verbose_name='视频课程')
    video = models.CharField(max_length=128, default='', blank=True, verbose_name='视频地址')
    video_length = models.CharField(max_length=16, default='', blank=True, verbose_name='视频长度')
    content = models.TextField(default='', blank=True, verbose_name='图文内容(markdown)')
    original_price = models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0, verbose_name='原价')
    current_price = models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0, verbose_name='现价')
    created = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    status = models.BooleanField(default=False, null=True, blank=True, verbose_name='是否上架')
    sale_earnings = models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0.8, verbose_name='分销收益')
    share_earnings = models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0.05, verbose_name='分享收益')
    share_discount = models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0.6, verbose_name='分享折扣')
    promotion_expire = models.DateTimeField(null=True, blank=True, verbose_name='优惠到期时间')
    is_promoted = models.BooleanField(default=False, verbose_name='是否加入促销')
    tag = models.ForeignKey(to=Tag, on_delete=models.SET_NULL, null=True, blank=True,
                            related_name='courses', verbose_name='标签')
    display_hot = models.IntegerField(default=300, null=True, verbose_name='显示热度')
    real_hot = models.IntegerField(default=0, null=True, verbose_name='真实热度')
    display_rank = models.DecimalField(max_digits=10, decimal_places=2, default=4.0, verbose_name='显示评分')
    real_rank = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name='真实评分')
    study_count = models.IntegerField(default=0, verbose_name='学习人数')
    favour_count = models.IntegerField(default=0, verbose_name='收藏人数')
    comment_count = models.IntegerField(default=0, verbose_name='评论人数')
    lecture_count = models.IntegerField(default=0, verbose_name='课时数')
    tech = models.CharField(max_length=256, default='', null=True, blank=True, verbose_name='技术栈')
    env = models.CharField(max_length=256, default='', null=True, blank=True, verbose_name='运行环境')
    banner = models.CharField(max_length=256, null=True, blank=True, verbose_name='课程横幅')
    video_status = models.BooleanField(default=False, verbose_name='转码完成')
    upload_thumbnail = models.ImageField(upload_to=UploadTo('thumbnail/'), null=True, blank=True, verbose_name='上传课程图')
    upload_banner = models.ImageField(upload_to=UploadTo('banner/'), null=True, blank=True, verbose_name='banner')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '课程列表'

    @property
    def paid(self):
        queryset = self.orders.all()
        for i in queryset:
            return i.paid

    @property
    def chapter(self):
        queryset = self.chapters.all()
        for i in queryset:
            res = []
            # sea = i.lectures.all()
            # for j in sea:
            #     rst = []
            #     rst.append(
            #         {
            #             "lecture_id": j.id,
            #             "title": j.title,
            #             "sort_index": j.sort_index,
            #             "is_free": j.is_free,
            #             "content": j.content,
            #             "video": j.video,
            #             "video_length": j.video_length,
            #         }
            #     )
            #     return rst
            res.append(
                {"chapter_id": i.id,
                 'title': i.title,
                 'sort_index': i.sort_index,
                 'lectures': [{
                    'lecture_id': j.id,
                    'title': j.title,
                    'sort_index': j.sort_index,
                    'is_free': j.is_free,
                    'video': j.video,
                    'content': j.content,
                    'video_length': j.video_length,
                    } for j in i.lectures.all()]
                 }
            )
            return res



#章节列表
class Chapter(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, related_name='chapters')
    sort_index = models.IntegerField(null=True, verbose_name='章节')
    title = models.CharField(max_length=256, blank=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '章节列表'

#课时列表
class Lecture(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='lectures')
    title = models.CharField(max_length=256, blank=False, verbose_name='标题')
    sort_index = models.IntegerField(null=True, verbose_name='课时')
    is_video = models.BooleanField(default=True, null=True, verbose_name='是否为视频')
    video = models.CharField(max_length=128, null=True, blank=True, verbose_name='课程视频')
    video_length = models.CharField(max_length=16, null=True, blank=True, verbose_name='视频长度')
    content = models.TextField(null=True, blank=True, verbose_name='图文内容(markdown)')
    is_free = models.BooleanField(default=False, verbose_name='是否免费')


    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '课时列表'

#课程数据
class CourseData(models.Model):
    course_classification_choice = (
        (0, '普通课程'),
        (1, '微课'),
        (2, 'Demo'),
        (3, '总量'),
    )

    course_classification = models.IntegerField(choices=course_classification_choice, verbose_name='课程类型')

    class Meta:
        verbose_name = '课程数据'

    def __str__(self):
        return self.get_course_classification_display()

