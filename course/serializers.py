'''{
    "id": 0,
    "title": "string",
    "target": "string",
    "thumbnail": "string",
    "banner": "string",
    "brief": "string",
    "desc": "string",
    "original_price": "string",
    "current_price": "string",
    "rank": 0,
    "study_count": 0,
    "favour_count": 0,
    "comment_count": 0,
    "promotion_expire": "string",
    "tech": "string",
    "env": "string",
    "content": "string",
    "status": true,
    "is_promoted": true,
    "video_length": "string"
  }'''
#课程列表
from rest_framework import serializers
from . import models
class CourseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = "__all__"


#课程详情
class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = "__all__"
#课程标签
class CourseTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = "__all__"



# #
# class CourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Course
#         fields = ["title", "study_count", "lecture_count", "paid", "video"]
# #
# class ChapterSerializer(serializers.ModelSerializer):
#     course = CourseSerializer
#     class Meta:
#         model = models.Chapter
#         fields = "__all__"
#
# #获取课程目录
# class CourseCatalogueSerializer(serializers.ModelSerializer):
#     chapter = ChapterSerializer()
#     class Meta:
#         model = models.Lecture
#         fields = '__all__'

#获取课程目录
class CourseCatalogueSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):  #对已有的字段加东西,对于没有的字段就去model类中定义
        ret = super().to_representation(instance)
        ret['tag'] = {
            'content': instance.tag.content,
            '2': 33333,
            '4': 4444,
        }
        return ret

    # chapter = ChapterSerializer()
    # def to_representation(self, instance):
    #     rst = []
    #     queryset = instance.chapters.lectures.all()   #获得lecture的查询集
    #     for i in queryset:
    #         rst.append({
    #             "lecture_id": i.id,
    #             "title": i.title,
    #             "sort_index": i.sort_index,
    #             "is_free": i.is_free,
    #             "content": i.content,
    #             "video": i.video,
    #             "video_length": i.video_length,
    #         })
    #     ret = super().to_representation(instance)
    #     ret['chapter'] = rst
    #     return ret


    class Meta:
        model = models.Course
        fields = ('title', 'study_count', 'lecture_count', 'paid', 'video', 'chapter', 'tag')




















#获取视频连接
class CourseVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lecture
        # fields = ['video', 'video_length', 'id']
        fields = '__all__'
#







