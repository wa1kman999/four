from rest_framework import serializers
from . import models


#文章详情序列化
class ArticleViewSerializer(serializers.ModelSerializer):
    # user = serializers.CharField(source="user.nick_name")  # 切记写在外面
    # user = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault()
    # )  不输入也不输出
    classification = serializers.CharField(source='classification.classification', read_only=True)
    user = serializers.SerializerMethodField()
    created = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S ')#还可以增加时间输出格式
    def get_user(self, obj):
        res = []
        res.append(obj.user.nick_name)
        res.append(obj.user.avatar_url)
        res.append(obj.user.desc)
        return res


    class Meta:
        model = models.Article
        # exclude = ('status', 'hot', 'tags', 'comment_count')
        fields = ['user', 'title', 'classification', 'created', 'brief']
    # model = models.Article
    # fields = "__all__"
    def validate(self, attrs):
        print(self.context['request'].user)
        print(attrs)
        return attrs


#/community
class CommunityViewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.nick_name")  #切记写在外面
    # user_password = serializers.CharField(source="user.password")  #切记写在外面  作者信息显示不全

    classification = serializers.CharField(source='classification.classification')

    class Meta:

        model = models.Article
        exclude = ('status', 'hot', 'tags', 'comment_count','content')
        # fields = "__all__"
        depth = 1


#/community/classification
class ArticleClassificationViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ArticleClassification
        exclude = ['level']

#发布文章 /community/article
class PutArticleViewSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default= serializers.CurrentUserDefault())
    classification = serializers.CharField(source='classification.classification', read_only=True)

    class Meta:
        model = models.Article
        fields = ['classification', 'title', 'content', 'brief', 'user']
        '''
        需要返回的字符串
        "classification": "string",
        "title": "string",
        "content": "string",
        "brief": "string",
        "pic": "string"'''

#文章回复
'''{
  "id": 0,
  "created": "string",
  "nickname": "string",
  "user_id": 0,
  "reply_to_nick": "string",
  "reply_to_id": "string",
  "content": "string"
}'''
class ReplyViewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    created = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    def get_user(self, obj):
        res = []
        res.append(obj.user.id)
        res.append(obj.user.nick_name)

    class Meta:
        model = models.CommentReply
        fields = ['user', 'created', 'reply_to', 'content']


        # '''
        #   "id": 0,
        #   "created": "string",
        #   "nickname": "string",
        #   "user_id": 0,
        #   "content": "string",
        #   "reply_count": "string"
        # }
        # '''
#文章的评论
class ArticleCommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.nick_name')
    # obj = article.article_comments.all()
    reply_count = serializers.SerializerMethodField()
    def get_reply_count(self, obj):
        print(obj.comment_replies)
        return obj.comment_replies.count()    #返回文章的评论数
    #
    # def get_reply_count(self, obj):
    #     aid = self.context['request'].query_params
    #     print(aid)
    #     article_obj = obj.Article.objects.filter(id=aid).first()
    #     print(article_obj)
    #     comments = article_obj.article_comments.order_by('-created')
    #     print(comments)
    #     reply_count = comments.comment_replys.count()
    #     print(reply_count)
    #     return reply_count

    class Meta:
        model = models.ArticleComment
        # exclude = ['user', ]
        fields = "__all__"




#文章点赞
class ArticleFavSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = ['id']

