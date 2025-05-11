<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { useCommonStore } from "../stores/common.store";
import PatientMainInfo from "../components/patient/PatientMainInfo.vue";
import PatientDetails from "../components/patient/PatientDetails.vue";
import PatientHealthIndicators from "../components/patient/PatientHealthIndicators.vue";
import ConnectPatient from "../components/patient/ConnectPatient.vue";
import { useRoute } from "vue-router";
import { useAxios } from "../composables/useAxios";

const patientStore = useCommonStore();
const {
    request: requestPatient,
    isLoading: isLoadingPatient,
    error: errorPatient,
} = useAxios();
const {
    request: requestHealth,
    isLoading: isLoadingHealth,
    error: errorHealth,
} = useAxios();

const patient = ref(null);
const source = ref(null);
const eventSource = ref(null);
const healthData = ref([]);

const route = useRoute();

const fetchPatient = async () => {
    patientStore.patientStatus = "Stable";
    const response = await requestPatient(
        `/patient/${route.params.id}`,
        "GET",
        null
    );
    if (response) {
        patient.value = response.patient;
        patientStore.patientStatus =
            patient.value.wound.infected === "Yes" ? "Critical" : "Stable";
    }
};

const connectPatient = async (file: File) => {
    if (!patient.value) return;

    // Create FormData for file upload
    const formData = new FormData();
    formData.append("file", file);

    try {
        // Send the file
        await requestHealth(
            `/patient/connect/${patient.value._id}`,
            "POST",
            formData
        );

        // Start SSE connection
        const apiUrl = import.meta.env.VITE_API_URL;
        eventSource.value = new EventSource(
            `${apiUrl}/patient/monitor/${patient.value._id}`
        );

        // Handle incoming data
        eventSource.value.onmessage = (event) => {
            const data = JSON.parse(event.data);
            healthData.value.push(data);

            // Update patient status based on infection status
            if (data.Infection === "Yes") {
                patientStore.patientStatus = "Critical";
            }
        };

        // Handle connection open
        eventSource.value.onopen = () => {
            source.value = true;
            healthData.value = []; // Reset health data
        };

        // Handle errors
        eventSource.value.onerror = (error) => {
            console.error("SSE Error:", error);
            eventSource.value?.close();
            eventSource.value = null;
        };
    } catch (error) {
        console.error("Error connecting patient:", error);
        eventSource.value?.close();
        eventSource.value = null;
    }
};

// Cleanup on component unmount
onUnmounted(() => {
    if (eventSource.value) {
        eventSource.value.close();
        eventSource.value = null;
    }
});

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
            <div
                v-if="isLoadingPatient"
                class="w-full flex items-center justify-center"
            >
                <i-line-md:loading-twotone-loop class="text-4xl" />
            </div>

            <div
                v-else-if="patient"
                class="w-full flex items-center justify-between"
            >
                <PatientMainInfo :patient="patient" />
                <PatientDetails :patient="patient" />
            </div>
        </div>

        <!-- health monitoring -->
        <div v-if="patient" class="mt-8">
            <div
                v-if="isLoadingHealth"
                class="w-full flex items-center justify-center"
            >
                <i-line-md:loading-twotone-loop class="text-4xl" />
            </div>

            <PatientHealthIndicators
                v-else-if="source && healthData.length"
                :data="healthData[healthData.length - 1]"
            />

            <ConnectPatient v-else @connect="connectPatient" />
        </div>
    </div>
</template>
