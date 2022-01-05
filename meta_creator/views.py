
from django.views.generic import TemplateView

from meta_creator.settings import META_VERSIONS
from meta_creator.forms import CreatorForm


class IndexView(TemplateView):
    template_name = 'meta_creator/index.html'
    extra_context = {"versions": META_VERSIONS.keys()}


class CreatorView(TemplateView):
    template_name = 'meta_creator/creator.html'
    metapath = None

    def get_context_data(self, **kwargs):
        return {'creator': CreatorForm(self.metapath.name)}
