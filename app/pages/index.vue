<script setup>

const { $io } = useNuxtApp();

const url = 'http://localhost:5000';
const times = ref(15);
const connections = ref({});
const isConnected = ref(false);
const currentClient = ref(0);
const messages = ref({});

const events = [
    'get_clients',
    'get_time',
    'get_since',
];

const connect = async () => {
    if (times.value < 1) return ;
    try {
        for (let i = 0; i < times.value; i+=1) {
            const socket = await $io.connect(url);
            connections.value[i] = socket;
            messages.value[i] = [];
            
            socket.on("connect", () => {
                console.log(socket.id);
            });

            socket.on("disconnect", () => {
                console.log(connections.value);
            });

            socket.on("message", (msg) => {
                messages.value[i].push(msg);
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
        delete connections.value[x];
        delete messages.value[x];
    });
    isConnected.value = false;
};

const emitEvent = async (event) => {
    connections.value[currentClient.value].emit(event);
};
</script>

<template>
    <div v-if="!isConnected">
        <input type="number" min="1" v-model="times" />
        <button @click="connect">Submit</button>
    </div>
    <div v-else>
        <button @click="disconnect">Disconnect</button>
        <div v-if="connections[currentClient]">
            Client {{ currentClient+1 }} {{ connections[currentClient].id }}
            <br />
            <input type="range" step="1" min="0" :max="times-1" v-model="currentClient" />
            <br />
            Events: <button v-for="(event, key) in events" :key="key" @click="emitEvent(event)">{{ event }}</button>
            <div v-for="(message, key) in messages[currentClient]" :key="key">
                <p>{{ message }}</p>
            </div>
        </div>
    </div>
</template>