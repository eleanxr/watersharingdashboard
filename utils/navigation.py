from django.http import HttpResponseRedirect

from django.core.urlresolvers import reverse

def maybe_redirect(request, response, obj):
    """Handle a query string that allows users to get redirected to a view after
    saving edits in the admin site. This function looks for a query string
    parameter called navsource. If that is set to 'main', then this function
    issues a redirect to the view named in the view_name parameter.
    """
    redirect_to_view = request.GET.get('navsource') == 'main'
    if (isinstance(response, HttpResponseRedirect) and redirect_to_view):
        response['location'] = obj.get_absolute_url()
    return response
