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
import axios from 'axios';

export default {
    name: 'DemoGame',
    components: {
        Block,
    },
    data() {
        return {
            players: [
                { name: 'Raprap', position: 3, level: 'boxed', },
                { name: 'Noel', position: 7, level: 'regular', },
                { name: 'Gohan', position: 8, level: 'regular', },
                { name: 'Robin', position: 9, level: 'regular', },
                { name: 'Dana', position: 10, level: 'regular', },
                { name: 'Adrian', position: 11, level: 'regular', },
                { name: 'Rowen', position: 12, level: {color: 'blue'}, },
            ],
        }
    },
    methods: {
        getPositionPlayer(position) {
            return this.players.find(x => x.position === position);
        },
        async getPlayersData() {
            try {
                const response = await axios.get("http://private-e7301-pygame.apiary-mock.com/players/");
                this.players = response.data;
                setTimeout(() => {
                    this.getPlayersData();
                }, 500);
            } catch(err) {
                alert('Something went wrong while requesting for the data. ' + err.message );
                // console.log( err.response.status );
            }
        }
    },
    mounted() {
        this.getPlayersData();
    }
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
