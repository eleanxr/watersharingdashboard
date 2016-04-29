from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse

from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response

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
    formsets : dict string -> Formset (optional)
        A dictionary mapping prefixes to Formset subclasses for related objects.
    title : string
        The title to use for the page.
    url_name : string
        The name of the URL to redirect to.
    redirect_url_name : string
        The name of the URL to redirect to after a successful POST.
    redirect_parameter_name : string
        The name of the identifier parameter for the redirect URL.
    additional_context : dict (optional)
        A dictionary of additional values to add to the template context.
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

    def dynamic_context(self, obj, form, formsets):
        """Allows subclasses to provide additional context dynamically.

        Override this method to provide an additional dictionary of context
        values.
        """
        return {}

    def _get_context(self, obj, form, formsets):
        context = {
            "object": obj,
            "title": self.title,
            "year": datetime.now().year,
            "post_url": reverse(self.url_name,
                kwargs={"object_id": obj.id}),
            "form": form,
        }
        if formsets:
            context.update(formsets)
        if hasattr(self, "additional_context"):
            context.update(self.additional_context)
        context.update(self.dynamic_context(obj, form, formsets))
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

class NewObjectView(View):
    """Generic view for creating a new object.

    Requires subclasses to define the following parameters:

    template_name : string
        The name of the template to render.
    model : Model subclass
        The Model that this view will be creating.
    form : tuple (string, Form subclass)
        A tuple with the render prefix and the edit form.
    formsets : dict string->Formset subclass
        A dictionary mapping names to formsets. The names are used as prefix
        values on the form and as names for the formsets in the page context.
    title : string
        The page title.
    url_name : string
        The name of the page url.
    redirect_url_name : string
        The name of the url to redirect to after a successful POST.
    redirect_parameter_name : string
        The name of the parameter identifying the object in the redirect view.
    additional_context : dict (optional)
        A dictionary of additional values to add to the template context.
    """

    def _validate_parameters(self):
        required_parameters = [
            'template_name',
            'model',
            'form',
            'formsets',
            'title',
            'redirect_url_name',
            'redirect_parameter_name',
        ]
        for parameter in required_parameters:
            if not hasattr(self, parameter):
                raise AttributeError(
                    "NewObjectView is missing required parameter " + parameter)

    def _get_context(self, form, formsets):
        context = {
            "title": self.title,
            "year": datetime.now().year,
            "post_url": reverse(self.url_name),
            "form": form,
        }
        if formsets:
            context.update(formsets)
        if hasattr(self, "additional_context"):
            context.update(self.additional_context)
        return context

    def __init__(self):
        self._validate_parameters()

    def get(self, request):
        form = self.form[1](prefix=self.form[0])
        formsets = {prefix: formset()
            for prefix, formset in self.formsets.items()
        }
        return render(request, self.template_name,
            self._get_context(form, formsets))

    def post(self, request):
        form = self.form[1](request.POST, prefix=self.form[0])
        formsets = {prefix: formset(request.POST)
            for prefix, formset in self.formsets.items()
        }

        formsets_valid = [f.is_valid() for f in formsets.values()]
        if form.is_valid() and all(formsets_valid):
            obj = form.save()
            for formset in formsets.values():
                formset.instance = obj
                formset.save()
            return redirect(self.redirect_url_name,
                **{self.redirect_parameter_name: obj.id})
        return render(request, self.template_name,
            self._get_context(form, formsets))
