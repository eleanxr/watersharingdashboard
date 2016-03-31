from django import forms

from .models import Scenario, CyclicTargetElement

class FormGroup(object):
    """A group of forms that can be validated and saved together.

    This class exposes each of the input forms as an attribute.

    Parameters
    ----------
    **forms : kwargs
        A set of forms and their names to be used as attribute values.
    """
    def __init__(self, **forms):
        self._forms = forms

    def _get_forms(self, names=None):
        """Get the forms, using an optional list of names.

        If names is not provided, then all forms are returned.
        """
        if names:
            return [self._forms[key] for key in names]
        else:
            return self._forms.values()

    def is_valid(self, names=None):
        """Check that all forms are valid, using an optional list of names.
        """
        forms = self._get_forms(names)
        return reduce(
            lambda a, b: a and b,
            map(lambda f: f.is_valid(), forms)
        )

    def save(self, names=None):
        """Save all the forms in the group, using an optional list of names to save.
        """
        forms = self._get_forms(names)
        for form in forms:
            form.save()

    def __getattr__(self, name):
        """Returns the form that was configured with the given name.
        """
        if self._forms.has_key(name):
            return self._forms[name]
        else:
            raise AttributeError("No such form " + name)

class ScenarioForm(forms.ModelForm):
    class Meta:
        model = Scenario
        fields = [
            "name",
            "description",
            "attribute_multiplier",
            "source_type",
        ]

class ScenarioGageForm(forms.ModelForm):
    class Meta:
        model = Scenario
        fields = [
            "gage_location",
            "parameter_code",
            "parameter_name",
            "start_date",
            "end_date",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={'class': 'datepicker'}),
            "end_date": forms.DateInput(attrs={"class": "datepicker"}),
        }

class ScenarioExcelForm(forms.ModelForm):
    class Meta:
        model = Scenario
        fields = [
            'excel_file',
            'sheet_name',
            'date_column_name',
            'attribute_column_name',
            'target_column_name',
        ]

CyclicTargetElementFormSet = forms.inlineformset_factory(
    Scenario, CyclicTargetElement,
    fields = [
        "from_month",
        "from_day",
        "to_month",
        "to_day",
        "target_value",
    ]
)
