$(function () {
    $('#logout').click(function (e) {
        e.preventDefault();
        $.ajax({
            url: "/api/logout",
            contentType: "application/json",
            dataType: "json",
            method: "POST",
            error: function (jqXHR, textStatus, errorThrown) {
                document.location.href = "/index";
            },
            success: function (data) {
                document.location.href = "/index";
            }
        })
    });
});