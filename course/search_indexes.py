from django.utils import timezone
from haystack import indexes
from .models import Course


class CourseIndex(indexes.SearchIndex, indexes.Indexable):
    #根据表中的哪些数据字段建立文件，把说明建在文件中
    text = indexes.CharField(document=True, use_template=True)

    # 建立的索引字段
    # title = indexes.CharField(model_attr="title")
    # user = indexes.CharField(model_attr="user")

    def get_model(self):
        return Course  # 返回课程模型

    # 建立索引数据
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
