<template>
    <div id="app">
        <demo-game />
    </div>
</template>

<script>
import DemoGame from './views/DemoGame.vue'

export default {
    name: 'app',
    components: {
        DemoGame,
    }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=Press+Start+2P');

#app {
    text-align: center;
}
</style>
