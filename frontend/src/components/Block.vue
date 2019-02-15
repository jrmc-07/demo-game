<template>
    <div class="block"> 
        <div v-if="player">
            {{number}}
            <div v-if="player" :style="levelStyle">
                <p v-text="player.name"></p>
            </div>
        </div>
        <div v-else class="number"> {{number}} </div>
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
            style_bordered: 'height: 100px; border: 5px black solid; border-radius: 25px;',
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
                    return `height: 100px; border: 5px gray solid; border-radius: 25px;`;
            }
        }
    }
}
</script>

<style scoped>
.block {
    height: 150px;
    width: 200px;
    border-radius: 25px;
    margin: auto;
}
.number {
    align-items: center;
    margin-top: 75px;
}
</style>
