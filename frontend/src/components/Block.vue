<template>
    <div class="block"> {{number}}
        <div v-if="player" :class="stateClass">
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
            //
        }
    },
    computed: {
        stateClass() {
            switch(this.player.state) {
                case 0:
                    return;
                case 1:
                    return "boxed";
                case 2:
                    return "boxed colored";
                default:
                    return;
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

