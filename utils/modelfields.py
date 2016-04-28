from django.db import models
from django.core.exceptions import ValidationError

from forms import DayOfYearFormField
from waterkit.flow.timeutil import DayOfYear

import re

class DayOfYearField(models.Field):
    """A custom form field to represent a day of the year as a
    month and day.
    """
    date_pattern = DayOfYearFormField.date_pattern

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 5
        super(DayOfYearField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(DayOfYearField, self).deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    def _parse(self, value):
        if not value:
            return value

        match = re.match(self.date_pattern, value)
        if not match:
            raise ValidationError(
                "Invalid day of year formatting in database '{:}'".format(value)
            )
        return DayOfYear(int(match.group('month')), int(match.group('day')))

    def from_db_value(self, value, expression, connection, context):
        if not value:
            return value
        return self._parse(value)

    def to_python(self, value):
        if not value:
            return value
        if isinstance(value, DayOfYear):
            return value
        return self._parse(value)

    def get_prep_value(self, value):
        value = super(DayOfYearField, self).get_prep_value(value)
        if not value:
            return value
        return str(value)

    def formfield(self, formclass=DayOfYearFormField, **kwargs):
        return super(DayOfYearField, self).formfield(formclass)

    def get_internal_type(self):
        return 'CharField'
