<template>
    <div class="popover popover-sm">
        <div class="popover-angle"></div>
        <div class="popover-inner">
            <div class="content-block">
                <p>{{message}}</p>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        props: ["message"]
    }
</script>