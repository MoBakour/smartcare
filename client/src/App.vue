<script setup lang="ts">
import { RouterView } from "vue-router";
</script>

<template>
    <div class="flex flex-col min-h-screen">
        <h1 class="p-2">SmartCare</h1>

        <main>
            <RouterView />
        </main>
    </div>
</template>
