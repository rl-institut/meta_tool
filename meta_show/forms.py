
import sqlahelper
from django import forms

from meta_show import models


class RunSelectionForm(forms.Form):
    def __init__(self, data=None):
        super(RunSelectionForm, self).__init__(data)

        session = sqlahelper.get_session()
        runs = session.query(models.Run).all()

        choices = [(run.run_id, run.timestamp) for run in runs]
        self.fields['runs'] = forms.ChoiceField(
            choices=choices,
            widget=forms.Select(attrs={'onChange': 'submit()'})
        )

    def get_first_run(self):
        try:
            return self.fields['runs'].choices[0][0]
        except IndexError:
            return None
