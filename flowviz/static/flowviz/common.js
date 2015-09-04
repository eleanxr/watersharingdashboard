(function (exports) {

    function CountDownLatch(count, done) {
        this.count = count;
        this.done = done;
    }
    exports.CountDownLatch = CountDownLatch;

    CountDownLatch.prototype.countDown = function() {
        if (--this.count == 0) {
            this.done();
        }
    }

    function downloadImage(imgUrl, imgId, done) {
        var image = document.getElementById(imgId);
        var downloadingImage = new Image();
        downloadingImage.onload = function () {
            image.src = this.src;
            done();
        };
        downloadingImage.src = imgUrl;
    }
    exports.downloadImage = downloadImage;

})(this.Common = {})
