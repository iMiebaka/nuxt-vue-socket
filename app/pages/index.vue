<script setup>

const { $io } = useNuxtApp();

const url = 'http://localhost:5000';
const times = ref(1);
const connections = ref({});
const isConnected = ref(false);

const connect = async () => {
    try {
        for (let i = 0; i < times.value; i+=1) {
            const socket = await $io.connect(url);
            console.log(connections.value, i)
            connections.value[i] = socket;
            
            socket.on("connect", () => {
                console.log(socket.id);
            });

            socket.on("disconnect", () => {
                console.log(connections.value);
            });
        }
        isConnected.value = true;
    } catch (err) {
        console.log(err);
    }
};

const disconnect = async () => {
    Object.keys(connections.value).forEach((x) => {
        connections.value[x].close();
    });
    isConnected.value = false;
};

</script>

<template>
    <div v-if="!isConnected">
        <input type="number" min="1" v-model="times" />
        <button @click="connect">Submit</button>
    </div>
    <button v-else @click="disconnect">Disconnect</button>
</template>