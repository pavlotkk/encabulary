<template>
    <form autocomplete="off">
        <div class="list-block inset">
            <ul>
                <slot></slot>
            </ul>
        </div>
        <slot name="footer"></slot>
    </form>
</template>

<script>
    export default {}
</script>
