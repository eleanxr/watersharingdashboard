from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse

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


class EditObjectView(View):
    """Class based view that provides an implementation for editing an object
    using a single form and optionally multiple formsets for related objects.

    The form will be passed to the template with the context name 'form' and
    each of the formsets will be passed to the template named by its prefix.

    When subclassing this view, you must define the following parameters:

    Parameters
    ----------
    template_name : string
        The name of the template to render.
    model : Model
        The Model subclass to edit.
    form : (string, Form)
        The prefix and Form subclass to use for the model.
    formsets : dict string -> Formset
        A dictionary mapping prefixes to Formset subclasses for related objects.
    title : string
        The title to use for the page.
    url_name : string
        The name of the URL to redirect to.
    redirect_url_name : string
        The name of the URL to redirect to after a successful POST.
    redirect_parameter_name : string
        The name of the identifier parameter for the redirect URL.
    """

    def _validate_parameters(self):
        required_parameters = [
            'template_name',
            'model',
            'form',
            'formsets',
            'title',
            'url_name',
            'redirect_url_name',
            'redirect_parameter_name',
        ]
        for parameter in required_parameters:
            if not hasattr(self, parameter):
                raise AttributeError(
                    "EditObjectView is missing required parameter " + parameter)

    def __init__(self):
        self._validate_parameters()

    def _get_context(self, obj, form, formsets):
        context = {
            "object": obj,
            "title": self.title,
            "year": datetime.now().year,
            "post_url": reverse(self.url_name,
                kwargs={"object_id": obj.id}),
            "form": form,
        }
        for prefix, formset in formsets.items():
            context[prefix] = formset
        return context

    def get(self, request, object_id):
        obj = get_object_or_404(self.model, pk=object_id)

        form = self.form[1](instance=obj, prefix=self.form[0])

        formsets = {}
        for prefix, formset_constructor in self.formsets.items():
            formsets[prefix] = formset_constructor(instance=obj, prefix=prefix)

        return render(
            request,
            self.template_name,
            self._get_context(obj, form, formsets)
        )

    def post(self, request, object_id):
        obj = get_object_or_404(self.model, pk=object_id)

        form = self.form[1](request.POST, instance=obj, prefix=self.form[0])

        formsets = {}
        for prefix, formset_constructor in self.formsets.items():
            formsets[prefix] = formset_constructor(request.POST,
                instance=obj, prefix=prefix)

        formsets_valid = map(lambda f: f.is_valid(), formsets.values())
        if (form.is_valid() and all(formsets_valid)):
            saved = form.save()
            for formset in formsets.values():
                formset.save()
            return redirect(self.redirect_url_name,
                **{self.redirect_parameter_name: saved.id})
        return render(
            request,
            self.template_name,
            self._get_context(obj, form, formsets)
        )
