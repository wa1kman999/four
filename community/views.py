from rest_framework import generics

from .seializers import ArticleViewSerializer, CommunityViewSerializer, ArticleClassificationViewSerializer, \
    PutArticleViewSerializer, ReplyViewSerializer
from community import models
from rest_framework.response import Response



#社区文章列表
from rest_framework import mixins
from rest_framework import viewsets
class ArticleViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin,viewsets.GenericViewSet):
    serializer_class = ArticleViewSerializer
    queryset = models.Article.objects.all()

    def get_serializer_class(self):
        if self.action in ['create']:
            return PutArticleViewSerializer
        return ArticleViewSerializer

    # def get(self,request, pk):
    #     # article = models.Article.objects.get(pk=pk)
    #     serializer = self.get_serializer(instance=self.get_object(), context={'request':request})
    #     data = serializer.data
    #     return Response({'msg': '获取单个文章成功', 'errorCode': 0, 'data': data})
    #
    # def put(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     if not serializer.is_valid():
    #         return Response({'MSG': '文本格式不对', 'errorCode': 2, 'data': {}})
    #     serializer.save()
    #     return Response({'MSG': '上传成功', 'errorCode': 0, 'data': {}})








#社区文章列表
class CommunityView(generics.GenericAPIView):
    serializer_class = CommunityViewSerializer
    def get(self, request):
        queryset = models.Article.objects.filter(status=True).order_by('-top', '-created')#选取最火和最新的发布的文章
        serializer = self.get_serializer(instance=queryset, many=True)
        data = serializer.data
        return Response({'msg': '文章获取成功', 'errorCode': 0, 'data': data})

#文章分类
class ArticleClassificationView(generics.GenericAPIView):
    serializer_class = ArticleClassificationViewSerializer

    def get(self, request):
        queryset = models.ArticleClassification.objects.order_by('-level')
        serializer = self.get_serializer(instance=queryset, many=True)
        data = serializer.data
        return Response({'MSG': '分类列表获取成功', 'errorCode': 0, 'data': data})



#获取回复
#
# class ReplyViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
#     serializer_class = ReplyViewSerializer
#     queryset = models.CommentReply.objects.all()


from .seializers import ArticleCommentSerializer
from .models import ArticleComment
# class ArticleCommentViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
#     serializer_class = ArticleCommentSerializer
#     queryset = models.ArticleComment.objects.all()
#
#     def get_object(self):
#         article_obj = models.Article.objects.filter(id=self.request.query_params.get('id'))
#         print(self.request.query_params.get('id'))
#         # print(article_obj)
#         return article_obj


        # comments = article_obj.article_comments.order_by('-created')
        # print(comments)
        # return comments
        # reply_count = comments.comment_replies.count()
        # print(reply_count)
        # return reply_count
        # print(models.ArticleComment.objects.filter(id=6))
        # return models.ArticleComment.objects.filter(id=6)
class ArticleCommentView(generics.GenericAPIView):
    # queryset = models.Article.objects.all()
    serializer_class = ArticleCommentSerializer

    def get(self, request, pk):
        article_obj = models.Article.objects.filter(id=pk).first()
        print(article_obj)
        comments = article_obj.article_comments.order_by('-created')
        print(comments)





        serializer = self.get_serializer(comments,many=True)
        return Response({'MSG': serializer.data})


        # aid = request.query_params
        # print(aid)
        # article_obj = models.Article.objects.filter(id=aid)
        # print(article_obj)
        # return Response({'MSG':'OK'})



from .seializers import ArticleFavSerializer
class ArticleFavViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin,viewsets.GenericViewSet):
    queryset = models.Article.objects.all()
    serializer_class = ArticleFavSerializer
#要想增加里面的信息 只需要重写update和destory即可
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()#这个是根据查询集出来的数据去选取输入的id值的
        print(instance)
        instance.fav_count = instance.fav_count + 1
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({'MSG': '点赞成功', 'data':serializer.data})
        # return Response({'MSG': '点赞成功'})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.fav_count = instance.fav_count - 1
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.save()
        return Response({'MSG': '取消点赞成功', 'data': serializer.data})









