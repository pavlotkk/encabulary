<template>
    <div id="learn" v-if="data.is_load">


        <div class="content-block-title">{{labelTitle}}</div>

        <div class="list-block" v-if="showWordView">
            <ul>
                <!-- words -->
                <li>
                    <div class="item-content">
                        <div class="item-inner">
                            <div class="content-block chip-content-block">
                                <div class="chip" v-for="word in data.current.words">
                                    <div class="chip-label">{{word}}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </li>
                <!-- transcription -->
                <li v-if="data.current.transcription">
                    <div class="item-content">
                        <div class="item-inner">
                            {{data.current.transcription}}
                        </div>
                    </div>
                </li>
                <!-- type_name -->
                <li v-if="data.current.type_name">
                    <div class="item-content">
                        <div class="item-inner">
                            {{data.current.type_name}}
                        </div>
                    </div>
                </li>
                <!-- answer -->
                <li>
                    <div class="item-content">
                        <div class="item-inner">
                            <div class="item-input">
                                <input type="text" placeholder="Answer" autofocus v-model="data.current.answer"
                                       @keyup.enter="showNextViewModel"/>
                            </div>
                        </div>
                    </div>
                </li>
            </ul>
            <!-- next -->
            <p class="form-button" @click="showNextViewModel">
                <a href="#" class="button">Next</a>
            </p>
        </div>

        <div class="list-block" v-if="showResultView">
            <!-- progress -->
            <div class="item-inner item-progress">
                <!--<progress-bar id="resultProgress" :value="resultProgressValue"></progress-bar>-->
                <progress-bar id="resultProgress" :value="resultProgressValue"></progress-bar>
            </div>
            <!-- result cards -->
            <div class="card" v-for="result in data.current.result.mistakes">
                <div class="card-header">
                    <div class="content-block chip-content-block">
                        <div class="chip chip-blue" v-for="word in result.correct">
                            <div class="chip-label">{{word}}</div>
                        </div>
                    </div>
                </div>
                <div class="card-content result-card-content">
                    <div class="content-block">
                        <div class="chip" v-for="word in result.translation">
                            <div class="chip-label">{{word}}</div>
                        </div>
                    </div>
                </div>
                <div class="card-footer">{{result.answer}}</div>
            </div>
            <!-- next -->
            <p class="form-button" @click="_nextViewModel">
                <a href="#" class="button">Next</a>
            </p>
        </div>

        <div class="list-block list-block-center" v-if="showFinalView">
            Congratulations! You learn 10 words. Press Continue to learn next words
            <!-- next -->
            <p class="form-button" @click="loadWords">
                <a href="#" class="button">Start</a>
            </p>
        </div>
    </div>
</template>

<script>
    import Vue from "vue";
    import VueResource from "vue-resource";
    import ProgressBar from "./f7/ProgressBar.vue";

    Vue.use(VueResource);

    const ORIGINAL_DIRECTION = 'original',
            USER_LANGUAGE_DIRECTION = 'user_language';

    export default {
        data(){
            return {
                endpoint: '/api/learn',
                loading: false,

                data: {
                    _index: -1,
                    _max_laps: 3,

                    is_load: false,
                    current: {
                        action_type: 'load-words',
                        words: []
                    },

                    actions: [],
                    answers: {
                        direction: '',
                        answers: []
                    }
                }
            }
        },
        created: function () {
            this.loadWords();
        },
        components: {ProgressBar},
        computed: {
            isAnswerEmpty: function () {
                if (this.data.current == null) {
                    return false;
                }

                return this.data.current.answer.trim().length == 0;
            },
            showWordView: function () {
                return this.data.current && ['repeat', 'learn'].includes(this.data.current.action_type);
            },
            showResultView: function () {
                return this.data.current && ['result'].includes(this.data.current.action_type);
            },
            showFinalView: function () {
                return this.data.current && ['final'].includes(this.data.current.action_type);
            },
            labelTitle: function () {
                let type = '';

                if(this.data.is_load && this.data.current != null){
                    type = this.data.current.action_type;
                }

                switch (type) {
                    case 'repeat':
                        return 'Repeat';
                    case 'learn':
                        return'Lean';
                    case 'commit':
                        return 'Submitting';
                    case 'result':
                        return 'Results';
                    case 'no-data':
                        return 'No data';
                    case 'load-words':
                        return 'Loading';
                    case 'final':
                        return 'Final';
                    default:
                        return '';
                }
            },
            resultProgressValue: function () {
                let value = 0;
                if (this.data.is_load && this.data.current != null && this.data.current.action_type != 'result') {
                    value = 100;
                }

                let result = this.data.current.result;
                let total = result.mistakes_count + result.ok_count;
                value = Math.round(result.ok_count * 100 / total);

                return value;
            }
        },
        methods: {
            loadWords: function () {
                if(this.loading){
                    return;
                }

                this._showLoading(true);
                this.data._index = -1;
                this.data.is_load = false;
                this.data.actions = [];
                this.data.answers.direction = '';
                this.data.answers.answers = [];
                this.data.current.action_type = 'load-words';

                this.$http.get(this.endpoint).then(function (response) {
                    this._showLoading(false);
                    const body = response.body;

                    if (body.error) {
                        this._alert(body.error);
                        return;
                    }

                    this.data.actions = this._transformWordsData(body.data);
                    this.data.is_load = true;

                    if (this.data.actions.length == 0) {
                        this.data.current.action_type = 'no-data';
                        return;
                    }

                    this._nextViewModel();
                }, function (response) {
                    this._showLoading(false);
                    this._alert("" + response.status + " " + response.statusText);
                });
            },
            showNextViewModel: function () {
                if (this.isAnswerEmpty) {
                    let self = this;
                    this.$f7.app.confirm('Are you sure?', function () {
                        self._saveAnswer();
                        self._nextViewModel();

                        if (self.data.current.action_type == 'commit') {
                            self.submitAnswers();
                        }
                    });
                    return;
                }

                this._saveAnswer();
                this._nextViewModel();

                if (this.data.current.action_type == 'commit') {
                    this.submitAnswers();
                }
            },
            submitAnswers: function () {
                if(this.loading){
                    return;
                }

                this._showLoading(true);

                var clonedData = this.data.answers.answers.map(function (item) {
                    return {
                        id_word: item.id_word,
                        answer: item.answer
                    }
                });

                var postData = {
                    direction: this.data.answers.direction,
                    answers: clonedData
                };

                this.data.answers.answers = [];

                this.$http.post(this.endpoint, postData).then(function (response) {
                    this._showLoading(false);
                    const body = response.body;

                    if (body.error) {
                        this._alert(body.error);
                        this._nextViewModel();
                        return;
                    }

                    this.data.current.result = this._transformResultData(body.data.result, postData.direction);
                    this.data.current.action_type = 'result';
                }, function (response) {
                    this._showLoading(false);
                    this._alert("" + response.status + " " + response.statusText);
                    this._nextViewModel();
                });
            },
            _transformWordsData: function (data) {
                let actions = [];

                if (data == null) {
                    return actions;
                }

                // add repeat actions
                if (data.repeat.length > 0) {
                    for (let repeat of data.repeat) {
                        actions.push({
                            action_type: 'repeat',
                            direction: USER_LANGUAGE_DIRECTION,
                            answer: '',
                            id_word: repeat.id_word,
                            transcription: repeat.transcription,
                            words: [repeat.word],
                            type_name: repeat.type_name
                        });
                    }

                    actions.push({
                        action_type: 'commit'
                    });

                    for (let repeat of data.repeat) {
                        actions.push({
                            action_type: 'repeat',
                            direction: ORIGINAL_DIRECTION,
                            answer: '',
                            id_word: repeat.id_word,
                            words: repeat.translations,
                            type_name: repeat.type_name
                        });
                    }

                    actions.push({
                        action_type: 'commit'
                    });
                }

                // add learn actions
                if (data.learn.length > 0) {
                    for (var lap = 0; lap < this.data._max_laps; lap++) {
                        for (let learn of data.learn) {
                            actions.push({
                                action_type: 'learn',
                                direction: USER_LANGUAGE_DIRECTION,
                                answer: '',
                                id_word: learn.id_word,
                                words: [learn.word],
                                transcription: learn.transcription,
                                type_name: learn.type_name
                            });
                        }

                        actions.push({
                            action_type: 'commit'
                        });

                        for (let learn of data.learn) {
                            actions.push({
                                action_type: 'learn',
                                direction: ORIGINAL_DIRECTION,
                                answer: '',
                                id_word: learn.id_word,
                                words: learn.translations,
                                type_name: learn.type_name
                            });
                        }

                        actions.push({
                            action_type: 'commit'
                        });
                    }
                }

                actions.push({
                    action_type: 'final'
                });

                return actions;
            },
            _transformResultData: function (data, direction) {
                let transformedData = [];

                if (data == null || data.mistakes.length == 0) {
                    return {
                        mistakes: transformedData,
                        mistakes_count: data.mistakes_count,
                        ok_count: data.ok_count
                    };
                }

                if (direction == USER_LANGUAGE_DIRECTION) {
                    for (let item of data.mistakes) {
                        transformedData.push({
                            answer: item.answer,
                            correct: item.correct,
                            translation: [item.translation]
                        });
                    }
                }
                if (direction == ORIGINAL_DIRECTION){
                    for (let item of data.mistakes) {
                        transformedData.push({
                            answer: item.answer,
                            correct: [item.correct],
                            translation: item.translation
                        });
                    }

                }

                return {
                    mistakes: transformedData,
                    mistakes_count: data.mistakes_count,
                    ok_count: data.ok_count
                };
            },
            _nextViewModel: function () {
                let dataNotLoad = !this.data.is_load;
                let noData = ++this.data._index >= this.data.actions.length;

                if (dataNotLoad || noData) {
                    this.data.current = null;
                    return;
                }

                this.data.current = this.data.actions[this.data._index];
            },
            _saveAnswer(){
                if (this.data.current == null) {
                    return;
                }

                this.data.answers.direction = this.data.current.direction;
                this.data.answers.answers.push({
                    id_word: this.data.current.id_word,
                    answer: this.data.current.answer
                });
            },
            _alert: function (message) {
                this.$f7.app.alert(message, "");
            },
            _showLoading: function(show){
                if(this.loading == show){
                    return;
                }

                this.loading = show;

                this.$f7.showLoading(this.loading);
            }
        }
    }
</script>

<style>
    #learn .chip-content-block {
        margin-top: 0;
        margin-bottom: 0;
        padding-left: 0;
    }

    #learn .form-button {
        margin: 35px 17px;
    }

    #learn .item-inner.item-progress {
        padding-left: 10px;
        padding-right: 10px;
        min-height: 10px;
    }
    #learn .item-inner.item-progress::after {
        background-color: #efeff4;
    }

    #learn .list-block-center{
        text-align: center;
    }

    #learn .chip.chip-blue {
        background: #007aff;
    }

    #learn .result-card-content{
        padding-top: 10px;
        padding-bottom: 10px;
    }
</style>