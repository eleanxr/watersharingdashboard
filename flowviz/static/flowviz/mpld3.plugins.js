
// RenderYear plugin
mpld3.register_plugin("renderyear", RenderYear);
RenderYear.prototype = Object.create(mpld3.Plugin.prototype);
RenderYear.prototype.constructor = RenderYear;
function RenderYear(fig, props){
    mpld3.Plugin.call(this, fig, props);
};

RenderYear.prototype.draw = function () {
    // FIXME: Kludgy way to get y axis
    var ax = this.fig.axes[0].elements[2];
    if (ax.axis) {
        ax.axis.tickFormat(d3.format("d"));
    }
    // HACK: use reset() to redraw figure.
    this.fig.reset();
}
    
// RenderPercent plugin
mpld3.register_plugin("renderpercent", RenderPercent);
RenderPercent.prototype = Object.create(mpld3.Plugin.prototype);
RenderPercent.prototype.constructor = RenderPercent;
function RenderPercent(fig, props){
    mpld3.Plugin.call(this, fig, props);
};

RenderPercent.prototype.draw = function () {
    // FIXME: Kludgy way to get y axis
    var ax = this.fig.axes[0].elements[1];
    if (ax.axis) {
        ax.axis.tickFormat(d3.format(",.1%"));
    }
    // HACK: use reset() to redraw figure.
    this.fig.reset();
}
