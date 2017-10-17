function initForm() {
    $('form').submit(function (e) {
        e.preventDefault();

        if (!validate()) {
            return;
        }

        showLoading(true);

        login({
            "email": $("#inputLogin").val().trim(),
            "password": $("#inputPassword").val().trim()
        }, {
            error: function (error) {
                showLoading(false);
                showError(error);
            },
            success: function (data) {
                showLoading(false);

                if(data.error == null){
                    document.location.href = "/learn";
                } else {
                    showError(data.error);
                }
            }
        })
    });
}

function validate() {
    showError(null);

    var login = $("#inputLogin").val().trim();
    var password = $("#inputPassword").val().trim();

    if(login == ""){
        showError("Login required");
        return false;
    }

    if(password == ""){
        showError("Password required");
        return false;
    }

    return true;
}

function showError(error) {
    if(error){
        $("#errorContainer").text(error);
        $("#errorContainer").show();
    } else {
        $("#errorContainer").hide();
    }
}

function showLoading(show) {
    var btn = $('#btnLogin');
    if(show){
        btn.text("Loading");
        btn.attr("disabled", true);
    } else {
        btn.text("Login");
        btn.removeAttr("disabled");
    }
}

function login(data, callback) {
    $.ajax({
        url: "/api/login",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(data),
        method: "POST",
        error: function(jqXHR, textStatus, errorThrown){
            callback.error(textStatus);
        },
        success: function (data) {
            callback.success(data);
        }
    })
}

$(function () {
    initForm();
    showLoading(false);
});