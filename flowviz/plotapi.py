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

class RenderYear(mpld3.plugins.PluginBase):
    """
    D3 plugin to render years without a comma.
    """
    JAVASCRIPT = """
    mpld3.register_plugin("renderyear", RenderYear);
    RenderYear.prototype = Object.create(mpld3.Plugin.prototype);
    RenderYear.prototype.constructor = RenderYear;
    function RenderYear(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    RenderYear.prototype.draw = function () {
        // FIXME: Kludgy way to get y axis
        var ax = this.fig.axes[0].elements[1];
        ax.axis.tickFormat(d3.format("d"));
        // HACK: use reset() to redraw figure.
        this.fig.reset();
    }
    """

    def __init__(self):
        self.dict_ = {"type": "renderyear"}

