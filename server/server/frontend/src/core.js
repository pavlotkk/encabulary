import Vue from 'vue'
import Framework7VuePlugin from "./f7-core";

function Vue7App(options) {
    Vue.use(Framework7VuePlugin);

    return new Vue(options);
}

export default Vue7App;
