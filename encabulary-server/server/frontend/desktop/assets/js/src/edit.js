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
        url: "/api/word",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(data),
        method: "POST",
        error: function(jqXHR, textStatus, errorThrown){
            if(jqXHR.status == 401){
                document.location.href = "/index";
                return;
            }
            callback.error(textStatus);
        },
        success: function (data) {
            if(data.error){
                callback.error(data.error);
            }
            callback.success(data);
        }
    })
}

function apiAutocomplete(word, word_type, callback) {
    var url = "/api/autocomplete/" + word;
    if(word_type != "" && word_type != 0){
        url += "/" + word_type;
    }
    $.ajax({
        url: url,
        method: "GET",
        error: function(jqXHR, textStatus, errorThrown){
            if(jqXHR.status == 401){
                document.location.href = "/index";
                return;
            }
            callback.error(textStatus);
        },
        success: function (data) {
            if(data.error){
                callback.error(data.error);
            }
            callback.success(data);
        }
    })
}

function editWord(id_word, data, callback) {
    $.ajax({
        url: "/api/word/" + id_word,
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(data),
        method: "PUT",
        error: function(jqXHR, textStatus, errorThrown){
            if(jqXHR.status == 401){
                document.location.href = "/index";
                return;
            }
            callback.error(textStatus);
        },
        success: function (data) {
            if(data.error){
                callback.error(data.error);
            }
            callback.success(data);
        }
    })
}

function deleteTranslation(id_translation, callback) {
    $.ajax({
        url: "/api/translation/" + id_translation,
        contentType: "application/json",
        dataType: "json",
        method: "DELETE",
        error: function(jqXHR, textStatus, errorThrown){
            if(jqXHR.status == 401){
                document.location.href = "/index";
                return;
            }
            callback.error(textStatus);
        },
        success: function (data) {
            if(data.error){
                callback.error(data.error);
            }
            callback.success(data);
        }
    })
}

function addTranslation(data, callback) {
    $.ajax({
        url: "/api/translation",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(data),
        method: "POST",
        error: function(jqXHR, textStatus, errorThrown){
            if(jqXHR.status == 401){
                document.location.href = "/index";
                return;
            }
            callback.error(textStatus);
        },
        success: function (data) {
            if(data.error){
                callback.error(data.error);
            }
            callback.success(data);
        }
    })
}

function deleteWord(id_word, callback) {
    $.ajax({
        url: "/api/word/" + id_word,
        contentType: "application/json",
        dataType: "json",
        method: "DELETE",
        error: function (jqXHR, textStatus, errorThrown) {
            if (jqXHR.status == 401) {
                document.location.href = "/index";
                return;
            }
            callback.error(textStatus);
        },
        success: function (data) {
            if(data.error){
                callback.error(data.error);
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
    modal.find("#inputTranscription").val(null);
    modal.find("#inputRu").tagsinput('removeAll');
    modal.find("#inputRu").val(null);
    modal.find("#inputPos").val("");
    modal.find("#inputEn").val(null);
    modal.find("#inputEn").focus();

    modal.find('#btnAdd').attr('disabled', null);

    modal.modal('hide');
}

function resetEditForm() {
    var modal = $("#editModal");
    modal.find("#inputIdWord").val(null);
    modal.find("#inputTranscription").val(null);
    modal.find("#inputRu").val(null);
    modal.find("#inputEn").val(null);
    modal.find("#inputEn").focus();

    modal.find('#btnEdit').attr('disabled', null);

    modal.modal('hide');
}

function initAddForm() {
    var modal = $("#addModal");

    modal.find('#btnAdd').click(function () {
       var data = {
           translations: modal.find("#inputRu").tagsinput('items'),
           word: modal.find("#inputEn").val().trim(),
           transcription: modal.find("#inputTranscription").val(),
           id_type: modal.find("#inputPos").val()
       };

        if(data.word == ""){ return; }

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

    modal.find('#btnAutocomplete').click(function () {
        var word = modal.find("#inputEn").val().trim(),
            word_type_id = modal.find("#inputPos").val();

        if(word == ""){ return; }

        apiAutocomplete(word, word_type_id, {
            error: function (errorText) {},
            success: function (data) {
                var word = data.data.word;
                modal.find("#inputPos").val(word.id_word_type);
                modal.find("#inputTranscription").val(word.transcription);

                var $tr = modal.find("#inputRu");
                $tr.tagsinput('removeAll');
                for(var i=0; i<word.translations.length; i++){ $tr.tagsinput('add', word.translations[i]); }
                $tr.tagsinput('refresh');
            }
        });
    });
}

function initEditForm() {
    var modal = $("#editModal");

    modal.find('#btnEdit').click(function () {
       var id_word = modal.find("#inputIdWord").val().trim();
       var data = {
           word: modal.find("#inputEn").val().trim(),
           transcription: modal.find("#inputTranscription").val(),
           id_type: modal.find("#inputPos").val()
       };

        if(data.word == ""){ return; }

        modal.find('#btnEdit').attr('disabled', 'disabled');
        editWord(id_word, data, {
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
    modal.find("#inputEn").val(data.word);
    modal.find("#inputTranscription").val(data.transcription);
    modal.find("#inputPos").val(data.id_type);

    var $tr = modal.find("#inputRu");
    $tr.tagsinput('removeAll');
    for(var i=0; i<data.translations.length; i++){ $tr.tagsinput('add', data.translations[i].translation); }
    $tr.tagsinput('refresh');

    $tr.off('itemRemoved');
    $tr.on('itemRemoved', function (event) {
        var id_tr = 0;
        for (var i=0; i<data.translations.length; i++){
            if(data.translations[i].translation == event.item){
                id_tr = data.translations[i].id;
                break;
            }
        }
        deleteTranslation(id_tr, {
            error: function (errorText) {
                showError(errorText);
            },
            success: function (data) {
            }
        });
    });

    $tr.off('itemAdded');
    $tr.on('itemAdded', function (event) {
        addTranslation({
                id_word: modal.find("#inputIdWord").val().trim(),
                translation: event.item
            },
            {
                error: function (errorText) {
                    showError(errorText);
                },
                success: function (resp) {
                    data.translations.push({
                        id: resp.data.id_translation,
                        translation: event.item
                    });
                }
            });
    });

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
            {
                data: "id_type",
                orderable: false,
                visible: false
            },
            {data: "type_name"},
            {
                data: "translations",
                orderable: false,
                render: function (data, type, full, meta) {
                    var length = full.translations.length;
                    if (length == 1) {
                        return full.translations[0].translation;
                    }

                    var template_parts = [];
                    template_parts.push('<ol class="row-ol">');
                    for (var i = 0; i < length; i++) {
                        template_parts.push('<li>' + full.translations[i].translation + '</li>');
                    }
                    template_parts.push('</ol>');
                    return template_parts.join("");
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
        $('#addModal').find('#inputEn').focus();
        $('#addModal').find('#inputRu').tagsinput('refresh');
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

        if(!confirm("Delete [" + deleteRow.id_word + "] '" + deleteRow.word + "' word?")){
            return;
        }

        deleteWord(deleteRow.id_word, {
            error: function (errorText) {
                showError(errorText);
            },
            success: function (data) {
                reloadDataTable();
            }
        });
    });
});