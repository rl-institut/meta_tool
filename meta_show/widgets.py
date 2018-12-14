
from abc import ABC
import sqlahelper

from django.utils.safestring import mark_safe
from django.forms.renderers import get_default_renderer

from meta_show.models import Meta


class CustomWidget(ABC):
    template_name: str = None

    def __str__(self):
        return self.render()

    def get_context(self):
        return {}

    def render(self):
        context = self.get_context()
        return self._render(self.template_name, context)

    @staticmethod
    def _render(template_name, context):
        renderer = get_default_renderer()
        return mark_safe(renderer.render(template_name, context))


class JsonWidget(object):

    def __init__(self, meta_id):
        self.meta = None
        if meta_id is not None:
            session = sqlahelper.get_session()
            self.meta = session.query(Meta).get(meta_id).json

    def __convert_to_html(self, data):
        html = ''
        if isinstance(data, dict):
            for key, value in data.items():
                html += f'<b>{key}:</b> {self.__convert_to_html(value)}'
        elif isinstance(data, list):
            html += '<ul>'
            for item in data:
                html += f'<li>{self.__convert_to_html(item)}</li>'
            html += '</ul>'
        else:
            html += f'{data}<br>'
        return html

    def render(self):
        return mark_safe(self.__convert_to_html(self.meta))
