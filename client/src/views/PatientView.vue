<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from "vue";
import { useCommonStore } from "../stores/common.store";
import PatientMainInfo from "../components/patient/PatientMainInfo.vue";
import PatientDetails from "../components/patient/PatientDetails.vue";
import PatientHealthIndicators from "../components/patient/PatientHealthIndicators.vue";
import ConnectPatient from "../components/patient/ConnectPatient.vue";
import { useRoute, useRouter } from "vue-router";
import { useAxios } from "../composables/useAxios";
import { toast } from "vue3-toastify";

const commonStore = useCommonStore();
const route = useRoute();
const router = useRouter();

const { request: requestPatient, isLoading: isLoadingPatient } = useAxios();
const { request: requestHealth, isLoading: isLoadingHealth } = useAxios();

const patient = ref<any>(null);
const connected = ref<boolean>(false);
const eventSource = ref<EventSource | null>(null);
const healthData = ref<any[]>([]);

const fetchPatient = async () => {
    commonStore.setPatientStatus("Stable");
    const response = await requestPatient(
        `/patient/${route.params.id}`,
        "GET",
        null
    );
    if (response) {
        patient.value = response.patient;
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

        connected.value = true;

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
                commonStore.setPatientStatus("Critical");
            }
        };

        // Handle connection open
        eventSource.value.onopen = () => {
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

const parsedAnalysis = computed(() => {
    const sections = patient.value.analysis.split("**").filter(Boolean);
    const htmlParts = [];

    for (let i = 0; i < sections.length; i += 2) {
        const title = sections[i].replace(":", "").trim();
        const body = sections[i + 1] || "";
        const bullets = body
            .split("\n")
            .map((line: string) => line.trim())
            .filter((line: string) => line.startsWith("*"))
            .map((line: string) => line.replace(/^\*+/, "").trim());

        htmlParts.push(
            `<h3 class="text-lg font-semibold">${title}</h3><ul class="pl-4">${bullets
                .map((b: string) => `<li class="text-gray-500">${b}</li>`)
                .join("")}</ul>`
        );
    }

    return htmlParts.join("");
});

// Cleanup on component unmount
onUnmounted(() => {
    if (eventSource.value) {
        eventSource.value.close();
        eventSource.value = null;
    }
});

onMounted(() => {
    fetchPatient();

    if (route.query.new) {
        toast.success("Patient added successfully", {
            onClose: () => {
                router.replace({ path: `/patients/${route.params.id}` });
            },
        });
    }
});
</script>

<template>
    <div class="mb-10">
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
                v-if="isLoadingHealth || (connected && healthData.length === 0)"
                class="w-full flex items-center justify-center"
            >
                <i-line-md:loading-twotone-loop class="text-4xl" />
            </div>

            <template v-else-if="connected && healthData.length">
                <PatientHealthIndicators :data="healthData" />

                <div class="mt-8 bg-gray-200 p-4 rounded-lg">
                    <h2
                        class="flex items-center gap-2 text-xl w-fit font-bold pb-2 bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-purple-500"
                    >
                        <span>AI Patient Analysis</span>
                        <i-mingcute:ai-fill class="text-2xl text-purple-500" />
                    </h2>
                    <div class="pl-4" v-html="parsedAnalysis"></div>
                </div>
            </template>

            <ConnectPatient v-else @connect="connectPatient" />
        </div>
    </div>
</template>
