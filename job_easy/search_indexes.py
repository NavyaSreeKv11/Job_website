from haystack import indexes

from .models import *


class JobIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = job
        excludes = ['user', 'post_date', 'applications']
    def get_model(self):
        return job
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
