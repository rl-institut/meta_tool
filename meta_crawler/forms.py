
from django import forms

from . import models


class RunSelectionForm(forms.Form):
    def __init__(self, data=None):
        super(RunSelectionForm, self).__init__(data)

        choices = []
        self.fields['runs'] = forms.ChoiceField(
            choices=choices,
            widget=forms.Select(attrs={'onChange': 'submit()'})
        )

    def get_first_run(self):
        try:
            return self.fields['runs'].choices[0][0]
        except IndexError:
            return None
