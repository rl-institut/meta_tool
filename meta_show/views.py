
import sqlahelper

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.defaults import bad_request

from meta_show import forms, models, widgets


class IndexView(TemplateView):
    template_name = 'meta_show/index.html'


class ShowView(TemplateView):
    template_name = 'meta_show/show.html'

    def get_context_data(self, run_form, run_id, **kwargs):
        context = super(ShowView, self).get_context_data(**kwargs)
        context['run_form'] = run_form

        # Get root:
        session = sqlahelper.get_session()
        run = session.query(models.Run).get(run_id)
        context['engines'] = run.sources
        return context

    def get(self, request, *args, **kwargs):
        run_form = forms.RunSelectionForm()
        run_id = run_form.get_first_run()
        context = self.get_context_data(run_form, run_id)
        return self.render_to_response(context)

    def post(self, request):
        run_form = forms.RunSelectionForm(request.POST)
        if run_form.is_valid():
            run_id = run_form.cleaned_data['runs']
        else:
            return bad_request(request, IndexError)
        context = self.get_context_data(run_form, run_id)
        return self.render_to_response(context)


def get_meta(request):
    meta_id = request.GET.get('meta_id')
    meta_widget = widgets.JsonWidget(meta_id)
    return HttpResponse(meta_widget.render())
