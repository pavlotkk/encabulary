<template>
    <div :id="id" class="progressbar" :data-value="value"><span></span></div>
</template>

<script>
    export default {
        props: ['value', 'id'],
        mounted: function () {
            this.$f7.app.showProgressbar(this.$f7.dom('#' + this.id), this.value);
        }
    }
</script>

<style>
</style>