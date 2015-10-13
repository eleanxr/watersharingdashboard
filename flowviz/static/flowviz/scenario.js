(function (exports) {

    function initialize(scenario, imgUrls) {
        // Set up the load indicator.
        $("#pleaseWaitDialog").modal();
        var imgCounter = new Common.CountDownLatch(Object.keys(imgUrls).length, function () {
            $("#pleaseWaitDialog").modal("hide");
        });

        function imgDone() {
            imgCounter.countDown();
        }
        
        function plot(id, url) {
            Common.mpld3Plot(id, url).always(imgDone);
        }


        var rasterTotalUrl = imgUrls.total + "?attribute=" + 
            encodeURIComponent(attribute_name) +
            "&cmap=spectral_r&title=" +
            "Flow+(cfs)" +
            "&logscale=True";
        plot("img-total", rasterTotalUrl);

        var rasterGapUrl = imgUrls.gap + "?attribute=" +
            encodeURIComponent(gap_attribute_name) +
            "&cmap=bwr_r&title=" +
            "Flow+gap+(cfs)" +
            "&zero=True";
        plot("img-gap", rasterGapUrl);

        plot("img-stats", imgUrls.stats);
        plot("img-stats-annual", imgUrls.stats_annual);
        plot("img-stats-pct", imgUrls.stats_pct);
        plot("img-stats-pct-annual", imgUrls.stats_pct_annual);
        plot("img-pct", imgUrls.pct);
        plot("img-pct-annual", imgUrls.pct_annual);

        plot("average-plot", dataUrls.average);
    }
    exports.initialize = initialize;

})(this.Scenario = {})
