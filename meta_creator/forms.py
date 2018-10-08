from django.forms import Form
from django_jsonforms.forms import JSONSchemaField


class CreatorForm(Form):
    meta = JSONSchemaField(
        schema='meta_v4.json',
        options={
            'theme': 'foundation6',
            'disable_collapse': True,
            'disable_properties': True
        }
    )
