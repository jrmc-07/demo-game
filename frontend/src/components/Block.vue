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
            style_bordered: 'border: 1px black solid',
        }
    },
    computed: {
        levelStyle() {
            if (typeof this.player.level == 'object') {
                return `
                    ${this.style_bordered};
                    background-color:${this.player.level.color};
                `;
            } else {
                if (this.player.level == 'boxed') {
                    return this.style_bordered;
                }
                return "";
            }
        }
    }
}
</script>

<style scoped>
.block {
    height: 70px;
    width: 70px;
}
.boxed {
    border: 1px;
    border-style: solid;
    border-color: black;
}
.colored {
    background-color: red;
}
</style>

