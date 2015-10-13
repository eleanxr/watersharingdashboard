
mpld3.register_plugin("renderyear", RenderYear);
RenderYear.prototype = Object.create(mpld3.Plugin.prototype);
RenderYear.prototype.constructor = RenderYear;
function RenderYear(fig, props){
    mpld3.Plugin.call(this, fig, props);
};

RenderYear.prototype.draw = function () {
    // FIXME: Kludgy way to get y axis
    var ax = this.fig.axes[0].elements[2];
    ax.axis.tickFormat(d3.format("d"));
    // HACK: use reset() to redraw figure.
    this.fig.reset();
}
