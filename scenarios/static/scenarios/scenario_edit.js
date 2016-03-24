(function ScenarioEdit(exports) {
    
    function chooseDataSourceForm(widget) {
        if (widget.val() === "GAGE") {
            $("#gage-parameters").show();
            $("#excel-parameters").hide();
        } else {
            $("#excel-parameters").show();
            $("#gage-parameters").hide();
        }
    }

    
    function initialize() {
        $(document).ready(function () {
            
            // Bootstrapify the form elements.
            $(".form-group > input, textarea, select").addClass("form-control");
            
            // Turn the datepickers into jquery ui choosers.
            $(".datepicker").datepicker({
                changeMonth: true,
                changeYear: true,
                dateFormat: "yy-mm-dd",
                minDate: new Date(1900, 1, 1),
                maxDate: 0
            });

            // Show the right form for the source type.
            chooseDataSourceForm($("#id_source_type"));
            $("#id_source_type").change(function () {
                chooseDataSourceForm($(this));
            });
        });
    }
    exports.initialize = initialize;

})(this.ScenarioEdit = {})
