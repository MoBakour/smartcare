<script setup lang="ts">
import { ref } from "vue";
import PatientMainInfo from "../components/patient/PatientMainInfo.vue";
import PatientDetails from "../components/patient/PatientDetails.vue";
import PatientHealthIndicators from "../components/patient/PatientHealthIndicators.vue";

const patient = ref({
    id: "ff763hjf92",
    name: "Amina Khoury",
    severity: "Moderate",
    condition: "Burn",
    location: "Elbow",
    status: "Stable",
    sex: "Female",
    age: 99,
    blood: "AB-",
    bed: "456",
    department: "Cardiology",
    checkIn: "23/12/25",
    systemNotes:
        "Patient is in stable condition — continue administering medication at the current dosage and interval.",
    expectedTimeToHeal: 7,
});
</script>

<template>
    <div>
        <!-- breadcrumb -->
        <div class="flex items-center gap-2">
            <router-link to="/patients" class="hover:underline"
                >Patients</router-link
            >
            <span>›</span>
            <span class="text-gray-500">{{ patient.name }}</span>
        </div>

        <!-- patient info -->
        <div class="flex items-center justify-between gap-10 mt-6">
            <!-- main info -->
            <PatientMainInfo :patient="patient" />

            <!-- details -->
            <PatientDetails :patient="patient" />
        </div>

        <!-- health indicators -->
        <PatientHealthIndicators :patient="patient" />
    </div>
</template>
