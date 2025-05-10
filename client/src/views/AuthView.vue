<script setup lang="ts">
import { ref } from "vue";
import Login from "../components/auth/Login.vue";
import Signup from "../components/auth/Signup.vue";

const showLogin = ref(true);
</script>

<template>
    <div>
        <!-- squares -->
        <div>
            <div
                class="w-[500px] h-[500px] bg-theme rounded-[80px] rotate-45 opacity-50 fixed top-0 -translate-x-1/3 -translate-y-1/8 pointer-events-none"
            />
            <div
                class="w-[500px] h-[500px] bg-theme rounded-[80px] rotate-45 fixed bottom-0 -translate-x-1/8 translate-y-1/3 pointer-events-none"
            >
                <!-- logo -->
                <img
                    src="../assets/images/logo.png"
                    alt="logo"
                    class="-rotate-45 opacity-60 w-[450px] relative -bottom-[25px]"
                />
            </div>
            <div
                class="w-[500px] h-[500px] bg-theme rounded-[80px] opacity-30 blur-3xl rotate-45 fixed right-0 translate-x-1/3 -translate-y-1/8 pointer-events-none"
            />
        </div>

        <!-- auth form container -->
        <div
            class="fixed right-0 w-3/5 flex flex-col items-center justify-center h-screen"
        >
            <Login v-if="showLogin" @switchToSignup="showLogin = false" />
            <Signup v-else @switchToLogin="showLogin = true" />
        </div>
    </div>
</template>
