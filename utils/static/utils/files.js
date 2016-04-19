(function (exports) {
    
    function uploadFile(postUrl, optionId) {

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
            $(optionId).append(
                $("<option />")
                .attr("value", data.id)
                .text(data.name)
            ).val(data.id);

            $("#upload-alert-placeholder").showAlert({
                title: "Upload Successful",
                message: "Your file has been saved.",
                level: "success",
            });
        }).fail(function () {
            $("#upload-alert-placeholder").showAlert({
                title: "Upload failed.",
                message: "Your file was not saved. Please try again.",
                level: "danger",
            });
        }).always(function (data) {
            $("#upload-wait-modal").modal('hide');
        });
    }
    exports.uploadFile = uploadFile;

    
})(this.Files = {})
