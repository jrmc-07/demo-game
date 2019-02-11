<template>
    <div class="flex-container block-container">
        <div v-for="i in players.length + 5" :key="i">
            <block v-if="getPositionPlayer(i)" 
                :player="getPositionPlayer(i)"
                :number="i" />
            <block v-else :number="i" />
        </div>
    </div>
</template>

<script>
import Block from '@/components/Block.vue';

export default {
    name: 'DemoGame',
    components: {
        Block,
    },
    data() {
        return {
            players: [
                { name: 'Raprap',
                    position: 6,
                    state: 0, },
                { name: 'Noel',
                    position: 7,
                    state: 0, },
                { name: 'Gohan',
                    position: 8,
                    state: 0, },
                { name: 'Robin',
                    position: 9,
                    state: 0, },
                { name: 'Dana',
                    position: 10,
                    state: 0, },
                { name: 'Adrian',
                    position: 11,
                    state: 0, },
                { name: 'Rowen',
                    position: 12,
                    state: 0, },
            ],
        }
    },
    methods: {
        getPositionPlayer(position) {
            return this.players.find(x => x.position === position);
        },
        getPlayersData() {
            //
        }
    },
}
</script>

<style scoped>
.flex-container {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: space-around;
    align-items: center;
}
.block-container {
    width: 70%;
    margin: auto;
}
</style>
