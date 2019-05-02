$(function () {
    const $formEvents = $("#form-events");
    const $formPlaceBet = $("#form-placebet");

    function placeBet(json) {
        $.ajax({
            type: "POST",
            url: "/play/placebet",
            data: JSON.stringify(json),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (data) {
                // showAlert(data['message'], "success");
                // $formEvents[0].reset();
                // $formPlaceBet[0].reset();
                location.reload()
            },
            error: function (errMsg) {
                showAlert(errMsg['responseJSON']['message'], "danger");
            }
        })
    }

    $formPlaceBet.on('submit', function (e) {
        e.preventDefault();
        let json = {
            "info": getFormData($formPlaceBet),
            "events": $formEvents.serializeArray()
        };
        placeBet(json)
    });

    function getFormData($form) {
        var unindexed_array = $form.serializeArray();
        var indexed_array = {};

        $.map(unindexed_array, function (n, i) {
            indexed_array[n['name']] = n['value'];
        });

        return indexed_array;
    }

    function randomChoice() {
        $formEvents.find('input').each(function () {

        });
    }
});