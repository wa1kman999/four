from django.db import models

class Banner(models.Model):
    name = models.CharField(max_length=128, verbose_name='横幅标题')
    img_url = models.CharField(max_length=256, verbose_name='横幅图片')
    link = models.CharField(max_length=256, null=True, blank=True, verbose_name='指向链接')
    level = models.IntegerField(default=0, verbose_name='显示顺序')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Activity(models.Model):
    name = models.CharField(max_length=128, verbose_name='活动标题')
    img_url = models.CharField(max_length=256, verbose_name='横幅图片')
    link = models.CharField(max_length=256, verbose_name='指向链接')

    class Meta:
        verbose_name = '活动'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class FriendLink(models.Model):
    name = models.CharField(max_length=16, verbose_name='网站')
    link = models.CharField(max_length=256, verbose_name='链接')
    level = models.IntegerField(default=0, verbose_name='显示顺序')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '友情连接'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
