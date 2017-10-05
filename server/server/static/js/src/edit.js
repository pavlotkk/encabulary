var wordsDataTable = null;

function toString(obj){
    if(Array.isArray(obj)){
        var length = obj.length;
        if(length == 1){
            return obj[0];
        }

        var template_parts = [];
        template_parts.push('<ol class="row-ol">');
        for(var i=0; i < length; i++){
            template_parts.push('<li>' + obj[i] + '</li>');
        }
        template_parts.push('</ol>');
        return template_parts.join("");
    }
    return obj;
}

function splitDateTime(strDateTime){
    if(strDateTime){
        return strDateTime.replace(' ', '<br/>')
    }

    return null;
}

function addWord(data, callback) {
    $.ajax({
        url: "/api/words/add",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(data),
        method: "POST",
        error: function(jqXHR, textStatus, errorThrown){
            callback.error(textStatus);
        },
        success: function (data) {
            if(!data.ok){
                if(data.error.code.indexOf("EAUTH") != -1){
                    document.location.href = "/index";
                    return;
                }
            }
            callback.success(data);
        }
    })
}

function editWord(data, callback) {
    $.ajax({
        url: "/api/words/edit",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(data),
        method: "POST",
        error: function(jqXHR, textStatus, errorThrown){
            callback.error(textStatus);
        },
        success: function (data) {
            if (!data.ok) {
                if (data.error.code.indexOf("EAUTH") != -1) {
                    document.location.href = "/index";
                    return;
                }
            }
            callback.success(data);
        }
    })
}

function deleteWord(data, callback) {
    $.ajax({
        url: "/api/words/delete",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(data),
        method: "POST",
        error: function(jqXHR, textStatus, errorThrown){
            callback.error(textStatus);
        },
        success: function (data) {
            if (!data.ok) {
                if (data.error.code.indexOf("EAUTH") != -1) {
                    document.location.href = "/index";
                    return;
                }
            }

            callback.success(data);
        }
    })
}

function showError(error) {
    if (error) {
        $("#errorContainer").text(error);
        $("#errorContainer").show();
    } else {
        $("#errorContainer").hide();
    }
}

function resetAddForm() {
    var modal = $("#addModal");
    modal.find("#inputEn").val(null);
    modal.find("#inputTranscription").val(null);
    modal.find("#inputRu").val(null);
    modal.find("#inputRu").focus();

    modal.find('#btnAdd').attr('disabled', null);

    modal.modal('hide');
}

function resetEditForm() {
    var modal = $("#editModal");
    modal.find("#inputIdWord").val(null);
    modal.find("#inputEn").val(null);
    modal.find("#inputTranscription").val(null);
    modal.find("#inputRu").val(null);
    modal.find("#inputRu").focus();

    modal.find('#btnEdit').attr('disabled', null);

    modal.modal('hide');
}

function initAddForm() {
    var modal = $("#addModal");

    modal.find('#btnAdd').click(function () {
       var data = {
           ru: modal.find("#inputRu").val().trim(),
           en: modal.find("#inputEn").val().trim(),
           en_transcription: modal.find("#inputTranscription").val(),
           en_pos: modal.find("#inputPos").val()
       };

        if(data.ru == ""){ return; }
        if(data.en == ""){ return; }

        modal.find('#btnAdd').attr('disabled', 'disabled');
        addWord(data, {
            error: function (errorText) {
                modal.find('#btnAdd').attr('disabled', null);
                showError(errorText);
                resetAddForm();
            },
            success: function (data) {
                resetAddForm();
            }
        });

    });
}

function initEditForm() {
    var modal = $("#editModal");

    modal.find('#btnEdit').click(function () {
       var data = {
           id: modal.find("#inputIdWord").val().trim(),
           ru: modal.find("#inputRu").val().trim(),
           en: modal.find("#inputEn").val().trim(),
           en_transcription: modal.find("#inputTranscription").val(),
           en_pos: modal.find("#inputPos").val()
       };

        if(data.ru == ""){ return; }
        if(data.en == ""){ return; }

        modal.find('#btnEdit').attr('disabled', 'disabled');
        editWord(data, {
            error: function (errorText) {
                modal.find('#btnEdit').attr('disabled', null);
                showError(errorText);
                resetEditForm();
            },
            success: function (data) {
                resetEditForm();
            }
        });

    });
}

function showEditForm(data) {
    var modal = $("#editModal");
    modal.find("#inputIdWord").val(data.id_word);
    modal.find("#inputRu").val(data.ru_word);
    modal.find("#inputEn").val(data.en_word);
    modal.find("#inputTranscription").val(data.en_transcription);
    modal.find("#inputPos").val(data.en_pos);

    modal.modal('show');
}

function initDataTable() {
    $.fn.dataTable.ext.errMode = 'none';

    wordsDataTable = $("#wordsTable").DataTable({
        processing: true,
        serverSide: true,
        destroy: true,
        order: [[6, "desc"]],
        ajax: {
            url: '/api/words/jqdatatable',
            type: 'POST',
            error: function (jqXHR, textStatus, errorThrown) {
                // is request aborted
                if (jqXHR.status == 0) {
                    return;
                }

                if(jqXHR.status == 401){
                    document.location.href = "/index";
                    return;
                }

                showError(jqXHR.status + " " + jqXHR.statusText);
            },
            dataSrc: function (data) {
                if(data.error){
                    showError(data.error);
                }
                showError(null);
                return data.data.table;
            }
        },
        columns: [
            // id_word
            {
                data: "id_word",
                render: function (data, type, full, meta) {
                    return full.id_word;
                }
            },
            {data: "word"},
            {data: "transcription"},
            {data: "type_name"},
            {
                data: "translations",
                orderable: false,
                render: function (data, type, full, meta) {
                    return toString(full.translations);
                }
            },
            {
                data: "score",
                render: function (data, type, full, meta) {
                    if (full.learn_score < 3) {
                        return full.learn_score;
                    } else if (full.learn_score >= 3 && full.learn_score < 6) {
                        return "<span class='text-primary'><b>" + full.learn_score + "</b></span>";
                    } else {
                        return "<span class='text-success'><b>" + full.learn_score + "</b></span>";
                    }
                }
            },
            {
                data: "add_db_dts",
                render: function (data, type, full, meta) {
                    return splitDateTime(full.add_db_dts);
                }
            },
            {
                data: "last_learn_db_dts",
                render: function (data, type, full, meta) {
                    return splitDateTime(full.last_learn_db_dts);
                }
            },
            {
                data: "repeat_db_dts",
                render: function (data, type, full, meta) {
                    return splitDateTime(full.repeat_db_dts);
                }
            },
            {
                data: null,
                orderable: false,
                render: function (data, type, full) {
                    return '<button type="button" class="btn btn-default btn-edit"> <span class="glyphicon glyphicon-edit" aria-hidden="true"></span> Edit </button>';
                }
            },
            {
                data: null,
                orderable: false,
                render: function (data, type, full) {
                    return '<button type="button" class="btn btn-danger btn-del"> <span class="glyphicon glyphicon-remove" aria-hidden="true"></span> Delete </button>';
                }
            }
        ]
    });
}

function reloadDataTable() {
    wordsDataTable.ajax.reload(null, false);
}

$(function () {
    showError(false);
    resetAddForm();
    resetEditForm();
    initAddForm();
    initEditForm();
    initDataTable();

    $('#addModal').on('shown.bs.modal', function () {
        $('#addModal').find('#inputRu').focus();
    });

    $('#addModal').on('hidden.bs.modal', function () {
        reloadDataTable();
    });

    $('#editModal').on('shown.bs.modal', function () {

    });

    $('#editModal').on('hidden.bs.modal', function () {
        reloadDataTable();
    });

    $("#dtContainer").on('click', '.btn-edit', function () {
        var editRow = wordsDataTable.row($(this).closest('tr')[0]).data();
        showEditForm(editRow);
    });

    $("#dtContainer").on('click', '.btn-del', function () {
        var deleteRow = wordsDataTable.row($(this).closest('tr')[0]).data();

        if(!confirm("Delete [" + deleteRow.id_word + "] '" + deleteRow.en_word + "' word?")){
            return;
        }

        deleteWord(deleteRow, {
            error: function (errorText) {
                showError(errorText);
            },
            success: function (data) {
                reloadDataTable();
            }
        });
    });
});