<script setup lang="ts">
import GeneralSettings from "../components/settings/GeneralSettings.vue";
import CriticalSettings from "../components/settings/CriticalSettings.vue";
</script>

<template>
    <div class="flex flex-col">
        <!-- page title -->
        <h1 class="flex items-center gap-2">
            <span class="text-2xl">Settings</span>
            <i-solar-arrow-right-outline class="text-2xl pt-1" />
        </h1>

        <!-- general settings -->
        <GeneralSettings />

        <!-- critical settings -->
        <CriticalSettings />
    </div>
</template>
