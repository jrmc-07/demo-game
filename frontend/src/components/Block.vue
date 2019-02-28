<template>
    <div>
        <div v-if="player">
            {{number}}
            <div class="nes-container is-dark" v-if="player" :style="levelStyle">
                <p class="nes-text" v-text="player.name"></p>
            </div>
        </div>
        <div v-else class="nes-text"> {{number}} </div>
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
    data: function() {
        return {
            style_bordered: 'height: 100px;',
        }
    },
    computed: {
        levelStyle() {
            switch(this.player.level) {
                case "CO":
                    return `
                        ${this.style_bordered};
                        background-color: ${this.player.color};
                    `;
                case "BX":
                    return this.style_bordered;
                case "RE":
                default:
                    return `height: 100px;`;
            }
        }
    }
}
</script>

<style scoped>
</style>
