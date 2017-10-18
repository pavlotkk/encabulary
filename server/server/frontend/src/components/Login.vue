<template>
    <form-view>
        <form-item>
            <input id="email" name="email" type="email" placeholder="Email" autofocus
                   v-model="email">
        </form-item>
        <form-item>
            <input id="password" name="password" type="password" placeholder="Password"
                   v-model="password" @keyup.enter="submit">
        </form-item>

        <div slot="footer" class="content-block" :class="{disabled: loading}">
            <p @click="submit"><a href="#" class="button">Login</a></p>
        </div>

    </form-view>

</template>

<script>
    import FormView from "./f7/Form.vue";
    import FormItem from "./f7/FormItem.vue";
    import Vue from "vue";
    import VueResource from "vue-resource";

    Vue.use(VueResource);

    export default {
        data(){
            return {
                email: '',
                password: '',
                loading: false,
                endpoint: '/api/login'
            }
        },
        computed: {
            emailIsEmpty: function () {
                return this.email.trim().length == 0;
            },
            passwordIsEmpty: function () {
                return this.password.trim().length == 0;
            }
        },
        methods: {
            showLoading: function(show){
                if(this.loading == show){
                    return;
                }

                this.loading = show;

                this.$f7.showLoading(this.loading);
            },

            submit: function () {
                let errorMessage = null;

                if (this.emailIsEmpty) {
                    errorMessage = 'Email required';
                } else if (this.passwordIsEmpty) {
                    errorMessage = 'Password required';
                }

                if (errorMessage != null) {
                    this._alert(errorMessage);
                    return;
                }

                this.showLoading(true);

                const options = this._getHttpOptions();

                this.$http.post(this.endpoint, options).then(function(response) {
                    this.showLoading(false);
                    const body = response.body;

                    if(body.error){
                        this._alert(body.error);
                        return;
                    }

                    this._redirectToNextPage();

                }, function (respose) {
                    this.showLoading(false);
                    this._alert("" + response.status + " " + response.statusText);
                });
            },
            _alert: function (message) {
                this.$f7.app.alert(message, "");
            },
            _getHttpOptions: function () {
                return {
                    email: this.email,
                    password: this.password
                };
            },
            _redirectToNextPage: function () {
                window.location = '/learn';
            }
        },
        components: {
            FormView,
            FormItem
        }
    }
</script>

<style>

</style>