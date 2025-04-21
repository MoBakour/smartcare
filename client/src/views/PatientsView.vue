<template>
    <div class="p-8">
        <h1>Patients</h1>
        <div class="mb-4">
            <router-link
                to="/add-patient"
                class="inline-block px-4 py-2 bg-green-500 text-white no-underline rounded-md hover:bg-green-600"
                >Add Patient</router-link
            >
        </div>
        <div>
            <!-- Patient list will be displayed here -->
            <p>List of patients will appear here</p>

            <!-- Example of how to link to a patient's details page -->
            <div class="py-2 border-b border-gray-200">
                <router-link
                    :to="`/patient/1`"
                    class="text-blue-500 hover:underline"
                    >John Doe</router-link
                >
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
// Patients list page logic will go here
</script>
