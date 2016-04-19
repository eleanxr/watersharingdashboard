(function (exports) {
    
    function chooseDataSource(widget) {
        if ($(widget).val() === 'NASS') {
            $("#nass-parameters").show();
            $("#excel-parameters").hide();
        } else {
            $("#nass-parameters").hide();
            $("#excel-parameters").show();
        }
    }
    
    function initialize() {
        
        // Make the Django formsets dynamic
        $(".years-formset").formset({
            addText: "Add year",
            deleteText: "Remove",
            prefix: "years",
        });
        
        $(".commodities-formset").formset({
            addText: "Add commodity",
            deleteText: "Remove",
            prefix: "commodities",
        });
        
        $(".groups-formset").formset({
            addText: "Add group",
            deleteText: "Remove",
            prefix: "groups",
        });

        // Use Select2 for crop groups.
        $('tr.groups-formset').find('select[multiple="multiple"]').select2();
        
        // Handle file uploads
        $("#upload-file-submit").click(function () {
            Files.uploadFile(fileUploadUrl, "#id_cropmix-excel_file");
        });

        // Handle switching between NASS and Excel data sources.
        chooseDataSource($("#id_cropmix-source_type"));
        $("#id_cropmix-source_type").change(function () {
            chooseDataSource($(this));
        });
        
    }
    exports.initialize = initialize
})(this.EditCropMix={})
