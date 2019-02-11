<template>
    <div class="block"> {{number}}
        <div v-if="player" :style="levelStyle">
            <p v-text="player.name"></p>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Block',
    props: {
        player: {
            type: Object,
            required: false,
        },
        number: {
            type: Number,
            required: true,
        }
    },
    data() {
        return {
            style_bordered: 'border: 5px black solid',
        }
    },
    computed: {
        levelStyle() {
            switch(this.player.level) {
                case "CO":
                    return `
                        ${this.style_bordered};
                        background-color:${this.player.color};
                    `;
                case "BX":
                    return this.style_bordered;
                case "RE":
                default:
                    return "border: 5px #ced6e2 solid";
            }
        }
    }
}
</script>

<style scoped>
.block {
    height: 100px;
    width: 150px;
    margin: auto;
}
</style>

