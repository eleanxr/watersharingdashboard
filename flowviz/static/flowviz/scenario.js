(function (exports) {

    var imgCounter = new Common.CountDownLatch(5, function () {
        $("#pleaseWaitDialog").modal("hide");
    });

    function initialize(scenario, imgUrls) {
        $("#pleaseWaitDialog").modal();
        downloadImage(imgUrls.average, "img-average")

        var rasterTotalUrl = imgUrls.total + "/?cmap=spectral_r&title=" +
            scenario.attribute_name + "+(" + scenario.attribute_units_abbr +
            ")&logscale=True";
        downloadImage(rasterTotalUrl, "img-total");

        var rasterGapUrl = imgUrls.gap + "/?cmap=bwr_r&title=" +
            scenario.attribute_name + "+gap+(" + scenario.attribute_units_abbr +
            ")&zero=True";
        downloadImage(rasterGapUrl, "img-gap");

        downloadImage(imgUrls.stats, "img-stats");
        downloadImage(imgUrls.pct, "img-pct");
    }
    exports.initialize = initialize;

    function downloadImage(imgUrl, imgId) {
        var image = document.getElementById(imgId);
        var downloadingImage = new Image();
        downloadingImage.onload = function () {
            image.src = this.src;
            imgCounter.countDown();
        };
        downloadingImage.src = imgUrl;
    }

})(this.Scenario = {})
