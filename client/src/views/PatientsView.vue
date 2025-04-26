<script setup lang="ts">
import { ref } from "vue";

const patients = ref([
    {
        id: 2,
        name: "Jane Smith",
        status: "Critical",
        condition: "Fracture",
    },
    {
        id: 4,
        name: "Bob Brown",
        status: "Critical",
        condition: "Burns",
    },
    {
        id: 3,
        name: "Alice Johnson",
        status: "Stable",
        condition: "Headache",
    },
    {
        id: 1,
        name: "John Doe",
        status: "Stable",
        condition: "Burns",
    },

    {
        id: 5,
        name: "Charlie Davis",
        status: "Stable",
        condition: "Fracture",
    },
]);
</script>

<template>
    <!-- top -->
    <div class="flex items-center justify-between">
        <!-- page title -->
        <h1 class="flex items-center gap-2">
            <span class="text-2xl">Patients</span>
            <i-solar-arrow-right-outline class="text-2xl pt-1" />
        </h1>

        <!-- add button -->
        <router-link
            to="/new"
            class="bg-theme text-white p-2 rounded-full transition hover:scale-105 cursor-pointer"
            title="Add Patient"
        >
            <i-mdi-plus class="text-2xl" />
        </router-link>
    </div>

    <!-- patients list -->
    <div class="mt-5 mb-15 flex flex-col items-center gap-6">
        <router-link
            :to="`/patients/${patient.id}`"
            v-for="patient in patients"
            :key="patient.id"
            class="w-[80%] p-6 rounded-2xl flex items-center bg-gradient-to-r transition-all hover:w-[82%] cursor-pointer"
            :class="
                patient.status === 'Critical'
                    ? 'from-crimson/40 to-crimson/20'
                    : 'from-theme/40 to-theme/20'
            "
        >
            <!-- user avatar -->
            <div
                class="w-[80px] h-[80px] bg-[#D9D9D9] rounded-full flex items-center justify-center"
            >
                <i-solar-user-outline class="text-5xl" />
            </div>

            <!-- user details -->
            <div class="flex flex-col ml-6">
                <p class="text-2xl font-semibold">{{ patient.name }}</p>
                <p
                    class="font-bold flex gap-3"
                    :class="
                        patient.status === 'Critical'
                            ? 'text-crimson'
                            : 'text-white'
                    "
                >
                    <span>{{ patient.status }}</span>
                    <span>|</span>
                    <span>{{ patient.condition }}</span>
                </p>
            </div>
        </router-link>
    </div>
</template>
