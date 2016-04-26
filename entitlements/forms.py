from django import forms
from django.forms import ValidationError

import re
import calendar

class DayOfYearFormField(forms.CharField):
    date_pattern = r'(?P<month>[01]?[0-9])[\-/](?P<day>[0-3]?[0-9])'

    def __init__(self, *args, **kwargs):
        super(DayOfYearFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = super(forms.CharField, self).clean(value)
        match = re.match(self.date_pattern, value)
        if not match:
            raise ValidationError("Day of year must be of the form MM-DD.")
        month = int(match.group('month'))
        day = int(match.group('day'))
        if month < 1 or month > 12:
            raise ValidationError("Months must be a number from 1 to 12.")

        # Don't pick a leap year below. Since this is to specify entitlements
        # that start on a particular day of each month in a year, we assume
        # nothing starts on Feb 29.
        days_in_month = calendar.monthrange(2015, month)[1]
        if day < 1 or day > days_in_month:
            raise ValidationError(
                "{:} has {:} days.".format(
                    calendar.month_name[month],
                    days_in_month
                )
            )
        return value

