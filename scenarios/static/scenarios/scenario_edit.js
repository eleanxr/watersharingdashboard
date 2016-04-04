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

    function uploadFile(postUrl) {

        // Hide the edit modal and show a progress modal.
        $("#upload-file-modal").modal('hide');
        $("#upload-wait-modal").modal('show');

        var formData = new FormData($("#upload-file-form")[0]);
        $.ajax({
            url: postUrl,
            data: formData,
            cache: false,
            // Required to correctly populate multipart content
            contentType: false,
            processData: false,
            type: "POST",
        }).done(function (data) {
            console.log("Upload done");
            console.log(data);

            $("#id_excel-excel_file").append(
                $("<option />")
                .attr("value", data.id)
                .text(data.name)
            ).val(data.id);
        }).always(function (data) {
            $("#upload-wait-modal").modal('hide');
        });
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
            uploadFile(fileUploadUrl);
        });
    }
    exports.initialize = initialize;

})(this.ScenarioEdit = {})
