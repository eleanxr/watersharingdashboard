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

        Common.downloadImage(imgUrls.average, "img-average", imgDone)

        var rasterTotalUrl = imgUrls.total + "?attribute=" +
            encodeURIComponent(attribute_name) +
            "&cmap=spectral_r&title=" +
            "Flow+(cfs)" +
            "&logscale=True";
        Common.downloadImage(rasterTotalUrl, "img-total", imgDone);

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
        Common.downloadImage(imgUrls.annual_min, "img-annual-trend", imgDone);
        Common.downloadImage(imgUrls.temporal_drought, "img-drought-temporal", imgDone);
        Common.downloadImage(imgUrls.volume_drought, "img-drought-volume", imgDone);
        Common.downloadImage(imgUrls.crop_area, "img-crop-area", imgDone);
        Common.downloadImage(imgUrls.crop_fraction, "img-crop-fraction", imgDone);
        Common.downloadImage(imgUrls.crop_revenue, "img-crop-revenue", imgDone);
        Common.downloadImage(imgUrls.crop_niwr, "img-crop-niwr", imgDone);
        Common.downloadImage(imgUrls.crop_revenue_per_af, "img-crop-revenue-per-af", imgDone);
        Common.downloadImage(imgUrls.crop_labor, "img-crop-labor", imgDone);
    }
    exports.initialize = initialize;

})(this.Scenario = {})
