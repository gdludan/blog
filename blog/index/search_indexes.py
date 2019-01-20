from haystack import indexes
from .models import Post
# 类名必须为模型名+Index，比如模型Post,则索引类为PostIndex
class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # 设置模型
    def get_model(self):
        return Post
    # 设置查询范围
    def index_queryset(self, using=None):
        return self.get_model().objects.all()