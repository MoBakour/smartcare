<script setup lang="ts">
import { RouterView } from "vue-router";
</script>

<template>
    <div class="flex flex-col min-h-screen">
        <nav
            class="flex justify-between items-center bg-slate-800 text-white px-8 py-4"
        >
            <div class="text-2xl font-bold">SmartCare</div>
            <div class="flex gap-6">
                <router-link
                    to="/patients"
                    class="text-white no-underline hover:text-gray-300"
                    :class="{
                        'font-bold border-b-2 border-white':
                            $route.path.includes('/patients'),
                    }"
                    >Patients</router-link
                >
                <router-link
                    to="/settings"
                    class="text-white no-underline hover:text-gray-300"
                    :class="{
                        'font-bold border-b-2 border-white':
                            $route.path === '/settings',
                    }"
                    >Settings</router-link
                >
                <router-link
                    to="/auth"
                    class="text-white no-underline hover:text-gray-300"
                    :class="{
                        'font-bold border-b-2 border-white':
                            $route.path === '/auth',
                    }"
                    >Login/Register</router-link
                >
            </div>
        </nav>

        <main class="flex-grow p-4">
            <RouterView />
        </main>
    </div>
</template>
