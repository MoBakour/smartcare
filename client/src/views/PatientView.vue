<template>
    <div class="p-8">
        <h1>Patient Details</h1>
        <div class="mb-4 text-gray-600">Patient ID: {{ $route.params.id }}</div>
        <div>
            <!-- Patient details content will go here -->
            <p>Patient information and medical history</p>
        </div>
        <div class="mt-8">
            <router-link
                to="/patients"
                class="inline-block px-4 py-2 bg-blue-500 text-white no-underline rounded-md hover:bg-blue-600"
                >Back to Patients</router-link
            >
        </div>
    </div>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";

const route = useRoute();
// You can use route.params.id to fetch the specific patient data
</script>
