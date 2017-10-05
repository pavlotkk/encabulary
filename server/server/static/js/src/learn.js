
// app

var LEARN_REPEATS = 3;
var REPEAT_LEARN_REPEATS = 1;
var answers = {};
var ORIGINAL_DIRECTION = 'original';
var USER_LANGUAGE_DIRECTION = 'user_language';

// server

function getServerWords(callback) {
    $.ajax({
        url: "/api/learn",
        contentType: "application/json",
        dataType: "json",
        method: "GET",
        error: function(jqXHR, textStatus, errorThrown){
            if(jqXHR.status == 401){
                document.location.href = "/index";
                return;
            }
            callback.error(textStatus);
        },
        success: function (data) {
            callback.success(data);
        }
    })
}
function rememberWords(ans, callback) {
    $.ajax({
        url: "/api/learn",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(ans),
        method: "POST",
        error: function(jqXHR, textStatus, errorThrown){
            if(jqXHR.status == 401){
                document.location.href = "/index";
                return;
            }
            callback.error(textStatus);
        },
        success: function (data) {
            callback.success(data);
        }
    })
}

// view

function showLoading(show) {
    show ? $("#loadingContainer").show() : $("#loadingContainer").hide();
}
function showError(error) {
    if(error){
        $("#errorContainer").text(error);
        $("#errorContainer").show();
    } else {
        $("#errorContainer").hide();
    }
}
function showWords(show) {
    show ? $("#wordsContainer").show() : $("#wordsContainer").hide();
}

// business

function toString(obj){
    if(Array.isArray(obj)){
        var length = obj.length;
        if(length == 1){
            return obj[0];
        }

        var template_parts = [];
        template_parts.push('<ol class="ol-row">');
        for(var i=0; i < length; i++){
            template_parts.push('<li>' + obj[i] + '</li>');
        }
        template_parts.push('</ol>');
        return template_parts.join("")
    }
    return obj;
}

function renderRepeatWords(words) {

    if(words.length == 0){
        return;
    }

    for(var repeat = 0; repeat < REPEAT_LEARN_REPEATS; repeat++){
        // en ru
        var en_ru_template = [];
        for(var i = 0; i < words.length; i++){
            var word = words[i];
            en_ru_template.push('<div data-type="user_language" data-id="' + word.id_word + '">');
            en_ru_template.push('<p class="repeat">Repeat</p>');
            en_ru_template.push('<h1 id="word-header" class="display-3">');
            en_ru_template.push(word.word);
            en_ru_template.push('</h1>');
            if(word.transcription){
                en_ru_template.push('<p id="word-transcription" class="lead">[');
                en_ru_template.push(toString(word.transcription));
                en_ru_template.push(']</p>');
            }
            if(word.type_name){
                en_ru_template.push('<p id="word-pos" class="lead">');
                en_ru_template.push(word.type_name);
                en_ru_template.push('</p>');
            }
            en_ru_template.push('<form id="form" autocomplete="off">');
            en_ru_template.push('<p><input id="userInput" class="form-control form-control-lg" type="text"></p>');
            en_ru_template.push('<p><button id="btnLearn" class="btn btn-lg btn-success" type="submit">Next</button></p>');
            en_ru_template.push('</form>');
            en_ru_template.push('</div>');
        }
        $('#wordsContainer').append(en_ru_template.join(""));

        // commit en ru
        var result_template = [];
        result_template.push('<div data-type="commit">');
        en_ru_template.push('<p class="repeat">Repeat</p>');
        result_template.push('<h1 class="display-3">Result</h1>');
        result_template.push('<p id="result">Loading...</p>');
        result_template.push('<p id="next" style="display: none;"><button id="btnNext" class="btn btn-lg btn-primary" type="button">Next</button></p>');
        result_template.push('</div>');
        $('#wordsContainer').append(result_template.join(""));

        // ru en
        var ru_en_template = [];
        for(var i = 0; i < words.length; i++){
            var word = words[i];
            ru_en_template.push('<div data-type="original" data-id="' + word.id_word + '">');
            en_ru_template.push('<p class="repeat">Repeat</p>');
            ru_en_template.push('<h1 id="word-header" class="display-3">');
            ru_en_template.push(toString(word.translations));
            ru_en_template.push('</h1>');
            ru_en_template.push('<form id="form" autocomplete="off">');
            ru_en_template.push('<p><input id="userInput" class="form-control form-control-lg" type="text"></p>');
            ru_en_template.push('<p><button id="btnLearn" class="btn btn-lg btn-success" type="submit">Next</button></p>');
            ru_en_template.push('</form>');
            ru_en_template.push('</div>');
        }
        $('#wordsContainer').append(ru_en_template.join(""));

        // commit ru en
        var result_template = [];
        result_template.push('<div data-type="commit">');
        en_ru_template.push('<p class="repeat">Repeat</p>');
        result_template.push('<h1 class="display-3">Result</h1>');
        result_template.push('<p id="result">Loading...</p>');
        result_template.push('<p id="next" style="display: none;"><button id="btnNext" class="btn btn-lg btn-primary" type="button">Next</button></p>');
        result_template.push('</div>');
        $('#wordsContainer').append(result_template.join(""));
    }

    // finish
    var finish_template = [];
    finish_template.push('<div data-type="finish-repeat" class="jumbotron">');
    en_ru_template.push('<p class="repeat">Repeat</p>');
    finish_template.push('<h1 class="display-3">Continue learning</h1>');
    finish_template.push('<p><button id="btnContinue" class="btn btn-lg btn-primary" type="button">Continue</button></p>');
    finish_template.push('</div>');
    $('#wordsContainer').append(finish_template.join(""));
}

function renderWords(words) {
    if(words.length == 0){
        renderNoWords();
        return;
    }

    for(var repeat = 0; repeat < LEARN_REPEATS; repeat++){
        // en ru
        var en_ru_template = [];
        for(var i = 0; i < words.length; i++){
            var word = words[i];
            en_ru_template.push('<div data-type="user_language" data-id="' + word.id_word + '">');
            en_ru_template.push('<h1 id="word-header" class="display-3">');
            en_ru_template.push(word.word);
            en_ru_template.push('</h1>');
            if(word.transcription){
                en_ru_template.push('<p id="word-transcription" class="lead">[');
                en_ru_template.push(word.transcription);
                en_ru_template.push(']</p>');
            }
            if(word.type_name){
                en_ru_template.push('<p id="word-pos" class="lead">');
                en_ru_template.push(word.type_name);
                en_ru_template.push('</p>');
            }
            en_ru_template.push('<form id="form" autocomplete="off">');
            en_ru_template.push('<p><input id="userInput" class="form-control form-control-lg" type="text"></p>');
            en_ru_template.push('<p><button id="btnLearn" class="btn btn-lg btn-success" type="submit">Next</button></p>');
            en_ru_template.push('</form>');
            en_ru_template.push('</div>');
        }
        $('#wordsContainer').append(en_ru_template.join(""));

        // commit en ru
        var result_template = [];
        result_template.push('<div data-type="commit">');
        result_template.push('<h1 class="display-3">Result</h1>');
        result_template.push('<p id="result">Loading...</p>');
        result_template.push('<p id="next" style="display: none;"><button id="btnNext" class="btn btn-lg btn-primary" type="button">Next</button></p>');
        result_template.push('</div>');
        $('#wordsContainer').append(result_template.join(""));

        // ru en
        var ru_en_template = [];
        for(var i = 0; i < words.length; i++){
            var word = words[i];
            ru_en_template.push('<div data-type="original" data-id="' + word.id_word + '">');
            ru_en_template.push('<h1 id="word-header" class="display-3">');
            ru_en_template.push(toString(word.translations));
            ru_en_template.push('</h1>');
            ru_en_template.push('<form id="form" autocomplete="off">');
            ru_en_template.push('<p><input id="userInput" class="form-control form-control-lg" type="text"></p>');
            ru_en_template.push('<p><button id="btnLearn" class="btn btn-lg btn-success" type="submit">Next</button></p>');
            ru_en_template.push('</form>');
            ru_en_template.push('</div>');
        }
        $('#wordsContainer').append(ru_en_template.join(""));

        // commit ru en
        var result_template = [];
        result_template.push('<div data-type="commit">');
        result_template.push('<h1 class="display-3">Result</h1>');
        result_template.push('<p id="result">Loading...</p>');
        result_template.push('<p id="next" style="display: none;"><button id="btnNext" class="btn btn-lg btn-primary" type="button">Next</button></p>');
        result_template.push('</div>');
        $('#wordsContainer').append(result_template.join(""));
    }

    // finish
    var finish_template = [];
    finish_template.push('<div data-type="finish" class="jumbotron">');
    finish_template.push('<h1 class="display-3">Congratulations! You learn 10 words. Press Continue to learn next words</h1>');
    finish_template.push('<p><button id="btnContinue" class="btn btn-lg btn-primary" type="button">Continue</button></p>');
    finish_template.push('</div>');
    $('#wordsContainer').append(finish_template.join(""));
}

function renderNoWords() {
    var template = '<div data-type="no-words"><h1 class="display-3">Nothing to learn :(</h1></div>';
    $('#wordsContainer').append(template);
}

function showNextWordContainer() {
    var container = $('#wordsContainer > div:first-child');
    container.show();

    var dataType = container.attr("data-type");
    if(dataType == "user_language"){
        showEnRu(container);
    } else if (dataType == "original"){
        showRuEn(container);
    } else if (dataType == "commit"){
        showCommit(container);
    } else if (dataType == "finish"){
        showFinish(container);
    } else if (dataType == "no-words"){

    } else if (dataType == "finish-repeat"){
        showFinishRepeat(container);
    } else {
        container.remove();
        showNextWordContainer();
    }
}

function showEnRu(container) {
    var btnLearn = container.find("#btnLearn");
    var input = container.find('#userInput');

    container.find("#form").submit(function (e) {
        e.preventDefault();

        var value = input.val().trim();
        var id = parseInt(container.attr("data-id"));

        if(value.length == 0 && !confirm("Skip this word?")){
            return;
        }

        if(answers.direction == null){
            answers.direction = USER_LANGUAGE_DIRECTION;
            answers.answers = []
        }

        answers.answers.push({id_word: id, answer: value});

        container.remove();
        showNextWordContainer();
    });
    input.focus();
}

function showRuEn(container) {
    var btnLearn = container.find("#btnLearn");
    var input = container.find('#userInput');

    container.find("#form").submit(function (e) {
        e.preventDefault();

        var value = input.val().trim();
        var id = parseInt(container.attr("data-id"));

        if(value.length == 0 && !confirm("Skip this word?")){
            return;
        }

        if(answers.direction == null){
            answers.direction = ORIGINAL_DIRECTION;
            answers.answers = []
        }

        answers.answers.push({id_word: id, answer: value});

        container.remove();
        showNextWordContainer();
    });
    input.focus();

}

function showCommit(container) {
    container.find("#btnNext").click(function () {
        container.remove();
        showNextWordContainer();

        answers = {};
    });

    rememberWords(answers, {
        error: function (errorText) {
            showError(errorText);
            container.find('#next').show();
        },
        success: function (data) {
            data = data.data.result;

            var table_template = [];
            table_template.push('<button type="button" class="btn btn-success">');
            table_template.push(data.ok_count);
            table_template.push('</button>');

            table_template.push('<button type="button" class="btn btn-danger">');
            table_template.push(data.mistakes_count);
            table_template.push('</button>');

            if(data.mistakes.length > 0){
                table_template.push('<table class="table table-condensed">');
                table_template.push('<thead>');
                table_template.push('<tr>');
                table_template.push('<th>Correct</th>');
                table_template.push('<th>Translate</th>');
                table_template.push('<th>Yours</th>');
                table_template.push('</tr>');
                table_template.push('</thead>');
                table_template.push('<tbody>');
                for(var i = 0; i < data.mistakes.length; i++){
                    table_template.push('<tr>');
                    table_template.push('<td>' + toString(data.mistakes[i].correct) + '</td>');
                    table_template.push('<td>' + toString(data.mistakes[i].translation) + '</td>');
                    table_template.push('<td>' + toString(data.mistakes[i].answer) + '</td>');
                    table_template.push('</tr>');
                }
                table_template.push('</tbody>');
                table_template.push('</table>');
            }

            container.find("#result").html(table_template.join(""));
            container.find('#next').show();
        }
    });
}

function showFinish(container) {
    container.find("#btnContinue").click(function () {
        container.remove();
        start();
    });
}

function showFinishRepeat(container) {
    container.find("#btnContinue").click(function () {
        container.remove();
        showNextWordContainer();
    });
}

function start() {
    answers = {};

    $("#wordsContainer").html("");

    showError(null);
    showLoading(true);
    showWords(false);

    getServerWords({
        error: function (errorText) {
            showLoading(false);
            showError(errorText);
        },
        success: function (data) {
            showLoading(false);
            onWordsLoaded(data.data);
        }
    });
}

// callbacks

function onWordsLoaded(words) {
    var repeatWords = words.repeat;
    var learnWords = words.learn;

    if(repeatWords.length > 0){
        renderRepeatWords(repeatWords);
    }

    renderWords(learnWords);
    showWords(true);
    showNextWordContainer();
}

// main

$(function () {
    start();
});