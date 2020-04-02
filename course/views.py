from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from . import serializers
from . import models
from .filters import CourseFilter
# 课程列表
from rest_framework import filters
from Utils.pagination import Pagination


from drf_haystack.viewsets import HaystackViewSet
from course.serializers import CourseIndexSerializer
from Utils.pagination import Pagination
from drf_haystack.filters import HaystackFilter, BaseHaystackFilterBackend
from .models import Course


#课程搜索的视图函数



class CourseSearchViewSet(HaystackViewSet):
    # 这是自己根据 PageNumberPagination 写的分页类，照样适用
    pagination_class = Pagination
    # 这里可以写多个模型，相应的：serializer里也可以写多个index_classes
    index_models = [Course, ]
    serializer_class = CourseIndexSerializer
    # 这时filter，这里用到了type
    # filter_backends = [HaystackFilter]
    # filter_fields = ("user", "title")
    # queryset = models.Course.objects.all()
    #
    # def get_queryset(self, index_models=[]):
    #     queryset = self.object_class()._clone()
    #     # 这时改写的get_queryset函数，用到了date_added
    #     # 如果上面没有把date_added和type加进去，这里是不能使用的
    #     queryset = queryset.models(*self.get_index_models()).order_by("-date_added")
    #     # queryset = queryset.models(*self.index_models).order_by("-date_added")
    #     return queryset
    #
    # def get_index_models(self):
    #     # 这是自己写的传入一个model参数，可以过滤掉不同的模型，配合上面的queryset使用
    #     model = self.request.query_params.get("model", None)
    #     di = {
    #         None: self.index_models,
    #         "topic": [Topic],
    #         "review": [Review]
    #     }
    #     return di.get(model, self.index_models)




class CourseInfoViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.CourseInfoSerializer
    queryset = models.Course.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = CourseFilter  # 记得在APP中注册filter
    search_fields = ('brief', 'user', 'title')
    ordering_fields = ('-created', '-display_hot', '-current_price', 'current_price', '-display_rank')
    pagination_class = Pagination


# 这里要用到过滤和筛选  待会学


# 课程详情
class CourseDetailViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.CourseDetailSerializer
    queryset = models.Course.objects.all()


# 课程标签
class CourseTagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.CourseTagSerializer
    queryset = models.Tag.objects.all()


# 获取课程列表
class CourseCatalogueViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.CourseCatalogueSerializer
    queryset = models.Course.objects.all()


# 获取视频连接
from .filters import LectureFilter


class CourseVideoViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.CourseVideoSerializer
    # queryset = models.Course.objects.all()  #这个是所有视频的集合
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = LectureFilter  # 记得在APP中注册filter
    search_fields = ('title')
    # 排序过滤(rest_frameworkfilters.OrderingFilter)
    ordering_fields = ('sort_index')

    # 此处应该返回的是检索的那个课程的所有视频集，重写get_queryset
    def get_queryset(self):
        quertset = models.Course.objects.all()
        return quertset

    def get_object(self):
        queryset = self.get_queryset()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        print(obj.id)  # 此处得到的是文章的id为2
        print(obj.brief)
        chapter = models.Chapter.objects.filter(course=obj.id)
        print(chapter[0])
        print(chapter[1])  # 这是一个章节的列表，一个文章有多个章节
        lecture1 = models.Lecture.objects.filter(chapter=chapter[0].id)
        # lecture2 = self.filter_queryset(lecture1)
        print(lecture1)
        # serializers.CourseVideoSerializer(instance=lecture1, many=rue)
        return lecture1

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)

    # def get_serializer(self, *args, **kwargs):
    #
    # def filter_queryset(self, queryset):
    #     for backend in list(self.filter_backends):
    #         queryset = backend().filter_queryset(self.request, queryset, self)
    #     return queryset
