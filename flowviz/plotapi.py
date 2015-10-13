from django.http import HttpResponse, HttpResponseBadRequest

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import mpld3
import mpld3.plugins

def __plot_to_response(fig):
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

def __plot_to_json_response(fig):
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='application/json')
    mpld3.save_json(fig, response)
    return response

__ACCEPT_MAP = {
    "application/json": __plot_to_json_response,
}

def render_plot(request, fig):
    """
    Render a matplotlib figure based on the accept header in an HTTP request.
    """
    handler = __ACCEPT_MAP.get(request.META.get("HTTP_ACCEPT"), __plot_to_response)
    return handler(fig)

