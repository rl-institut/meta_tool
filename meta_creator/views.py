
from django.views.generic import TemplateView

from meta_creator.forms import CreatorForm


class CreatorView(TemplateView):
    template_name = 'meta_creator/creator.html'

    def get_context_data(self, **kwargs):
        return {'creator': CreatorForm()}
