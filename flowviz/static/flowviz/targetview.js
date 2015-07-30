var TargetView = ( function (window, undefined) {

    function initialize() {
        $('.img-wrapper > img').on('load', function () {
            imgLoaded(this)
        })
    }

    function imgLoaded(img) {
        var $img = $(img);
        $img.parent().addClass('loaded');
    }

    return {
        initialize: initialize
    }

})(window)
