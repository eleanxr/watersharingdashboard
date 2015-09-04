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

})(this.Common = {})
