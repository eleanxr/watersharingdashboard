var TargetView = ( function (window, undefined) {

    function initialize() {
    }

    function imgLoaded(img) {
        var $img = $(img);
        $img.parent().addClass('loaded');
    }

    return {
        initialize: initialize
    }

})(window)
