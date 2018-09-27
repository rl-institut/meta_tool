
from django.views.generic import TemplateView

from meta_show import forms


class ShowView(TemplateView):
    template_name = 'meta_show/meta_show.html'

    def get_context_data(self, **kwargs):
        context = super(ShowView, self).get_context_data(**kwargs)
        context['run_selection'] = forms.RunSelectionForm()
        return context
