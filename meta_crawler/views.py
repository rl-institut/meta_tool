
from collections import namedtuple

from django.http import HttpResponse
from django_filters.views import FilterView

from . import models, widgets, filters


MetaItem = namedtuple("MetaItem", ["id", "title", "name"])


class IndexView(FilterView):
    template_name = 'meta_crawler/index.html'
    filterset_class = filters.MetaFilter

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        # FIXME: Look only at latest run!
        # TODO: More & better filters
        context['metas'] = [
            MetaItem(meta.id, meta.title, meta.name) for meta in self.object_list
        ]
        return context


def get_meta(request):
    meta_id = request.GET.get('meta_id')
    metadata = models.Meta.objects.get(id=meta_id).metadata
    meta_widget = widgets.JsonWidget(metadata)
    return HttpResponse(meta_widget.render())
