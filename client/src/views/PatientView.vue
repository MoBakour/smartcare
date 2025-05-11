<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useCommonStore } from "../stores/common.store";
import PatientMainInfo from "../components/patient/PatientMainInfo.vue";
import PatientDetails from "../components/patient/PatientDetails.vue";
import PatientHealthIndicators from "../components/patient/PatientHealthIndicators.vue";
import { useRoute } from "vue-router";
import { useAxios } from "../composables/useAxios";

const patientStore = useCommonStore();
const { request, isLoading, error } = useAxios();

const patient = ref(null);

const route = useRoute();

const fetchPatient = async () => {
    patientStore.patientStatus = "Stable";
    const response = await request(`/patient/${route.params.id}`, "GET", null);
    if (response) {
        patient.value = response.patient;
        patientStore.patientStatus = patient.value.wound.infected
            ? "Critical"
            : "Stable";
    }
};

onMounted(() => {
    fetchPatient();
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
            <span class="text-gray-500">{{ patient?.name || "..." }}</span>
        </div>

        <!-- patient info -->
        <div class="flex items-center justify-between gap-10 mt-6">
            <!-- loader -->
            <div
                v-if="isLoading"
                class="w-full flex items-center justify-center"
            >
                <i-line-md:loading-twotone-loop class="text-4xl" />
            </div>

            <template v-if="!isLoading && patient">
                <!-- main info -->
                <PatientMainInfo :patient="patient" />

                <!-- details -->
                <PatientDetails :patient="patient" />
            </template>
        </div>

        <!-- health indicators -->
        <PatientHealthIndicators
            v-if="!isLoading && patient"
            :patient="patient"
        />
    </div>
</template>
