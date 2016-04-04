(function ($) {
    // A jQuery plugin for dynamically showing a bootstrap alert element.
    $.fn.showAlert = function (options) {
        $.extend({
            title: "",
            message: "",
            level: "info",
        }, options);

        this.append(
            $("<div />")
            .addClass("alert alert-dismissible fade in")
            .addClass("alert-" + options.level)
            .attr("role", "alert")
            .append(
                $("<button></button>")
                .attr('type', 'button')
                .addClass("close")
                .attr('data-dismiss', 'alert')
                .attr('aria-label', 'Close').append(
                    $("<span aria-hidden='true'>x</span>")
                )
            ).append(
                $("<h4>" + options.title + "</h4>")
            ).append(
                $("<p></p>").text(options.message)
            )
        ).alert();

        return this;
    }
} (jQuery));
