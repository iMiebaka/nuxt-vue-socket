import { io } from "socket.io-client";
import { defineNuxtPlugin } from '#app';

export default defineNuxtPlugin((nuxtApp) => {
    nuxtApp.provide('io', io);
});