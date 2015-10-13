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

        var rasterTotalUrl = imgUrls.total + "?attribute=" + 
            encodeURIComponent(attribute_name) +
            "&cmap=spectral_r&title=" +
            "Flow+(cfs)" +
            "&logscale=True";
        Common.downloadImage(rasterTotalUrl, "img-total", imgDone);
        // Common.mpld3Plot("raster-total", rasterTotalUrl);

        var rasterGapUrl = imgUrls.gap + "?attribute=" +
            encodeURIComponent(gap_attribute_name) +
            "&cmap=bwr_r&title=" +
            "Flow+gap+(cfs)" +
            "&zero=True";
        Common.downloadImage(rasterGapUrl, "img-gap", imgDone);

        Common.downloadImage(imgUrls.stats, "img-stats", imgDone);
        Common.downloadImage(imgUrls.stats_annual, "img-stats-annual", imgDone);
        Common.downloadImage(imgUrls.stats_pct, "img-stats-pct", imgDone);
        Common.downloadImage(imgUrls.stats_pct_annual, "img-stats-pct-annual", imgDone);
        Common.downloadImage(imgUrls.pct, "img-pct", imgDone);
        Common.downloadImage(imgUrls.pct_annual, "img-pct-annual", imgDone);

        Common.mpld3Plot("average-plot", dataUrls.average);
    }
    exports.initialize = initialize;

})(this.Scenario = {})
