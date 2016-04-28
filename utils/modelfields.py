from django.db import models

from forms import DayOfYearFormField

import re

class DayOfYear(object):
    """Represents a day of the year as a month/day pair.
    """
    def __init__(self, month, day):
        self.month = month
        self.day = day

    def __str__(self):
        return "{:0>2}-{:0>2}".format(self.month, self.day)

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
        match = re.match(self.date_pattern, value)
        if not match:
            raise models.ValidationError("Invalid day of year formatting in database.")
        return DayOfYear(int(match.group('month')), int(match.group('day')))

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return self._parse(value)

    def to_python(self, value):
        if isinstance(value, DayOfYear):
            return value
        if value is None:
            return value
        return self._parse(value)

    def get_prep_value(self, value):
        return str(value)

    def formfield(self, formclass=DayOfYearFormField, **kwargs):
        return super(DayOfYearField, self).formfield(formclass)

    def get_internal_type(self):
        return 'CharField'
