
from django.views.generic import TemplateView
from django.views.defaults import bad_request

from meta_show import forms, crawler


class IndexView(TemplateView):
    template_name = 'meta_show/index.html'


class CrawlerView(TemplateView):
    template_name = 'meta_show/crawler.html'

    def post(self, request):
        if 'crawl' in request.POST:
            crawler.get_meta_from_db()
            return self.get(request)


class ShowView(TemplateView):
    template_name = 'meta_show/show.html'

    def get_context_data(self, run_form, run_id, **kwargs):
        context = super(ShowView, self).get_context_data(**kwargs)
        context['run_form'] = run_form
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
