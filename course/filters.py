import django_filters
from .models import Course
from .models import Lecture


class CourseFilter(django_filters.rest_framework.FilterSet):
    '''课程的过滤类'''
    target = django_filters.ChoiceFilter(choices=Course.target_choice)  # 课程分类

    class Meta:
        model = Course
        fields = ['target']


#
class LectureFilter(django_filters.rest_framework.FilterSet):
    '''课时的过滤类'''

    # chapter = django_filters.CharFilter(field_name='chapter_id')
    # lecture = django_filters.CharFilter(field_name='lecture_id')

    # class Meta:
    #     model = Course
    #     fields = ['id']
    # help_text--docs：description
    # pricemin=django_filters.NumberFilter(field_name='shop_price',lookup_expr='gte',help_text='最低价格')
    # pricemax=django_filters.NumberFilter(field_name='shop_price',lookup_expr='lte')
    # # name=django_filters.CharFilter(field_name='name',lookup_expr='icontains')
    # lecture =django_filters.NumberFilter(method='lecture_filter')
    # #定制的过滤方法
    # def lecture_filter(self, queryset, name, value):
    #     return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))
    class Meta:
        model = Course
        fields = ['id']
