from django.shortcuts import render

from django.views.generic import View

from datetime import datetime

class BaseView(View):
    """A base class that populates common information that all views need."""
    context = {
        'year': datetime.now().year,
    }

    def get_context(self, **kwargs):
        context = self.context
        for name, value in kwargs.iteritems():
            context[name] = value
        return context
