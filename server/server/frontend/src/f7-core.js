class Framework7App {
    constructor() {
        this.app = new Framework7();
        this.dom = Dom7;
        this.view = this.app.addView('.view-main', {
            dynamicNavbar: true
        });
    }

    showLoading(show = true, type = "indicator") {
        switch (type) {
            case "indicator":
                if (show) {
                    this.app.showIndicator();
                } else {
                    this.app.hideIndicator();
                }
                break;
            case "progress-infinite":
                var container = this.dom('body');
                if (container.children('.progressbar, .progressbar-infinite').length) {
                    break;
                }

                if (show) {
                    this.app.showProgressbar(container);
                    break;
                }

                this.app.hideProgressbar();
                break;
        }
    }
}

const Framework7VuePlugin = {
    install(Vue, options) {
        Vue.prototype.$f7 = new Framework7App()
    }
};

export default Framework7VuePlugin;
