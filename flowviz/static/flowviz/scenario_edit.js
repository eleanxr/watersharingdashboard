var ScenarioEdit = (function(window, undefined) {
    function initialize() {
        $("#gage").hide();
        $("#excel").hide();

        $("#id_source_type").change(function(evt) {
            if ($(this).val() == "GAGE") {
                $("#gage").show();
                $("#excel").hide();
            } else if ($(this).val() == "XLSX") {
                $("#gage").hide();
                $("#excel").show();
            } else {
                $("#gage").hide();
                $("#excel").hide();
            }
        });

        $("#id_source_type").change();
    }

    return {
        initialize: initialize
    }
})(window)
