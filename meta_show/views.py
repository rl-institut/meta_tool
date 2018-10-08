
import sqlahelper
from django.views.generic import TemplateView
from django.views.defaults import bad_request

from meta_show import forms, models


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
            run_id = run_form['runs']
        else:
            return bad_request(request, IndexError)
        context = self.get_context_data(run_form, run_id)
        return self.render_to_response(context)


class JsonView(TemplateView):
    template_name = 'includes/json_item.html'

    def get_context_data(self, meta_id):
        if meta_id is None:
            return {}
        session = sqlahelper.get_session()
        meta = session.query(models.Meta).get(meta_id)
        return {'data': meta.json}

    def get(self, request, *args, **kwargs):
        meta_id = request.GET.get('meta_id', None)
        context = self.get_context_data(meta_id)
        return self.render_to_response(context)
