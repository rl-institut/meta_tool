
import django_filters

from meta_crawler.models import Meta


class MetaFilter(django_filters.FilterSet):
    class Meta:
        model = Meta
        fields = ['tags']
