from django.db import models
from user.models import User


# 文章分类
class ArticleClassification(models.Model):
    classification = models.CharField(max_length=32, verbose_name='文章分类')
    level = models.IntegerField(default=0, verbose_name='显示优先级')
    icon = models.CharField(max_length=64, default='', verbose_name='图标地址')
    official = models.BooleanField(default=False, verbose_name='官方文章')

    def __str__(self):
        return self.classification

    class Meta:
        verbose_name = '文章分类'


# 文章标签
class ArticleTag(models.Model):
    tag = models.CharField(max_length=32, verbose_name='文章标签')

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = '文章标签'


# 文章
class Article(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='articles', verbose_name='作者')
    title = models.CharField(max_length=128, blank=False, verbose_name='标题', )
    brief = models.TextField(blank=True, null=True, verbose_name='简介')
    content = models.TextField(verbose_name='内容', )
    tags = models.ManyToManyField(to=ArticleTag, related_name='articles', blank=True, verbose_name='标签')
    classification = models.ForeignKey(to=ArticleClassification, null=True,
                                       on_delete=models.CASCADE, related_name='articles', verbose_name='分类')
    thumbnail = models.CharField(max_length=128, null=True, blank=True, verbose_name='缩略图')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    hot = models.IntegerField(default=0, verbose_name='热度')
    fav_count = models.IntegerField(default=0, verbose_name='赞')
    comment_count = models.IntegerField(default=0, verbose_name='评论数')
    status = models.BooleanField(default=True, null=True, verbose_name='是否发布')
    top = models.BooleanField(default=False, null=True, verbose_name='是否置顶')
    essence = models.BooleanField(default=False, null=True, verbose_name='精华')

    # "id": 0,
    # "classification": "string",
    # "brief": "string",
    # "title": "string",
    # "created": "string",
    # "fav_count": "string",
    # "thumbnail": "string",
    # "top": true,
    # "essence": true,
    # "content": true,
    # "author":

    def __str__(self):
        return str(self.title)


# 文章收藏
class ArticleFavour(models.Model):
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE, related_name='favour')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='article_favour')
    created = models.DateTimeField(auto_now_add=True, )


# 文章评论
class ArticleComment(models.Model):
    user = models.ForeignKey(to=User, null=True, on_delete=models.CASCADE, related_name='article_comments')
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE, related_name='article_comments')
    content = models.CharField(max_length=1024, verbose_name='评论内容')
    created = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')


# 评论回复
class CommentReply(models.Model):
    user = models.ForeignKey(to=User, null=True, on_delete=models.CASCADE, related_name='comment_replies')
    comment = models.ForeignKey(to=ArticleComment, on_delete=models.CASCADE, related_name='comment_replies')
    reply_to = models.ForeignKey(to='CommentReply', null=True, on_delete=models.CASCADE,
                                 related_name='replies')
    content = models.CharField(max_length=512, verbose_name='评论内容')
    created = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
