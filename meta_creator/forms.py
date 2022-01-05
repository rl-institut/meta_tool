from django.forms import Form
from django_jsonforms.forms import JSONSchemaField


class CreatorForm(Form):
    def __init__(self, metajson):
        super(CreatorForm, self).__init__()
        self.fields["meta"] = JSONSchemaField(
            schema=f"metajsons/{metajson}",
            options={
                'theme': 'foundation6',
                'disable_collapse': True,
                'disable_properties': True
            }
        )
