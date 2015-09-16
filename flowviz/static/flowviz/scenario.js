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

        var rasterTotalUrl = imgUrls.total + "/?cmap=spectral_r&title=" +
            scenario.attribute_name + "+(" + scenario.attribute_units_abbr +
            ")&logscale=True";
        Common.downloadImage(rasterTotalUrl, "img-total", imgDone);

        var rasterGapUrl = imgUrls.gap + "/?cmap=bwr_r&title=" +
            scenario.attribute_name + "+gap+(" + scenario.attribute_units_abbr +
            ")&zero=True";
        Common.downloadImage(rasterGapUrl, "img-gap", imgDone);

        Common.downloadImage(imgUrls.stats, "img-stats", imgDone);
        Common.downloadImage(imgUrls.stats_annual, "img-stats-annual", imgDone);
        Common.downloadImage(imgUrls.stats_pct, "img-stats-pct", imgDone);
        Common.downloadImage(imgUrls.stats_pct_annual, "img-stats-pct-annual", imgDone);
        Common.downloadImage(imgUrls.pct, "img-pct", imgDone);
        Common.downloadImage(imgUrls.pct_annual, "img-pct-annual", imgDone);
    }
    exports.initialize = initialize;

})(this.Scenario = {})
