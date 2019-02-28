<template>
    <div class="nes-container is-dark full-container">
        <div class="nes-text title"> CoP: RankUp! </div>
        <div class="nes-container is-dark is-rounded">
            <div v-for="i in players.length + 5" :key="i">
                <block v-if="getPositionPlayer(i)"
                       :player="getPositionPlayer(i)"
                       :number="i" />
                <block v-else :number="i" />
            </div>
        </div>
    </div>
</template>

<script>
import Block from '@/components/Block.vue';
import axios from 'axios';

export default {
    name: 'DemoGame',
    components: {
        Block,
    },
    data: function() {
        return {
            players: [],
        }
    },
    methods: {
        getPositionPlayer(position) {
            return this.players.find(x => x.position === position);
        },
        async getPlayersData() {
            const api = "http://127.0.0.1:8000/players/";
            await axios.get(api)
                .then((response) => {
                    this.players = response.data;
                }).catch((err) => {
                    alert('Something went wrong while requesting for the data. ' + err.message );
                });
            setTimeout(() => {
                this.getPlayersData();
            }, 500);
        },

    },
    mounted: function() {
        this.getPlayersData();
    }
}
</script>

<style scoped>
.title {
    font-size: 40px;
}

.full-container {
    height: 100vh;
}

.nes-container.is-dark.is-rounded {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    align-items: center;
}
</style>
