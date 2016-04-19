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

        // The fields for the Excel or Gage data sources are required if the
        // field is visible, so just mark them as required.
        $("#gage-parameters, #excel-parameters")
            .find("span.required-label").text("(required)");

        // Show the right form for the source type.
        chooseDataSourceForm($("#id_scenario-source_type"));
        $("#id_scenario-source_type").change(function () {
            chooseDataSourceForm($(this));
        });

        // Make the flow target form dynamic.
        $(".target-formset").formset({
            addText: "Add Target",
            deleteText: "Remove",
            prefix: cyclicTargetPrefix,
        });

        // Handle file uploads.
        $("#upload-file-submit").click(function () {
            Files.uploadFile(fileUploadUrl, "#id_scenario-excel_file");
        });
    }
    exports.initialize = initialize;

})(this.ScenarioEdit = {})
