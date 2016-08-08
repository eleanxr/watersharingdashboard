from django.http import HttpResponse

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import calendar

def new_figure():
    fig = Figure()
    ax = fig.add_subplot(111)
    return (fig, ax)

def plot_to_response(fig):
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

def to_percent(y, position):
    s = str(100 * y)
    # The percent symbol needs escaping in latex
    if matplotlib.rcParams['text.usetex'] == True:
        return s + r'$\%$'
    else:
        return s + '%'

def to_month(x, position):
    return calendar.month_abbr[position]
