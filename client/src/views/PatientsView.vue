<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useAxios } from "../composables/useAxios";

const { request, isLoading, error } = useAxios();
const patients = ref([]);

const fetchPatients = async () => {
    const response = await request("/patient/all", "GET", null);
    if (response) {
        patients.value = response.patients
            .map((patient: IPatient) => {
                return {
                    ...patient,
                    avatarUrl: computed(() => {
                        if (!patient.avatar) return null;

                        return `${
                            import.meta.env.VITE_API_URL
                        }/patient/avatar/${patient._id}`;
                    }),
                };
            })
            .sort((a, b) => {
                const aInfected = a.wound.infected === "Yes";
                const bInfected = b.wound.infected === "Yes";

                if (aInfected && !bInfected) return -1;
                if (!aInfected && bInfected) return 1;
                return 0;
            });
    }
};

onMounted(() => {
    fetchPatients();
});
</script>

<template>
    <!-- top -->
    <div class="flex items-center justify-between relative">
        <!-- page title -->
        <h1 class="flex items-center gap-2">
            <span class="text-2xl">Patients</span>
            <i-solar-arrow-right-outline class="text-2xl pt-1" />
        </h1>

        <!-- add button -->
        <router-link
            to="/new"
            class="bg-theme text-white p-2 rounded-full transition hover:scale-105 cursor-pointer absolute right-0 top-1/2 -translate-y-1/2"
            title="Add Patient"
        >
            <i-mdi-plus class="text-2xl" />
        </router-link>
    </div>

    <!-- loading state -->
    <div v-if="isLoading" class="mt-10 flex justify-center">
        <i-line-md:loading-twotone-loop class="text-4xl" />
    </div>

    <!-- error state -->
    <div v-else-if="error" class="mt-10 text-center text-red-500">
        {{ error }}
    </div>

    <!-- no patients found -->
    <p
        class="text-gray-500 text-center mt-10"
        v-else-if="patients.length === 0"
    >
        No patients found
    </p>

    <!-- patients list -->
    <div v-else class="mt-10 mb-15 flex flex-col items-center gap-6">
        <router-link
            :to="`/patients/${patient._id}`"
            v-for="patient in patients"
            :key="patient._id"
            class="w-[80%] p-6 shadow-xl rounded-2xl flex items-center bg-gradient-to-r transition-all hover:w-[82%] cursor-pointer"
            :class="
                patient.wound.infected === 'Yes'
                    ? 'from-crimson/35 to-crimson/15'
                    : 'from-theme/45 to-theme/25'
            "
        >
            <!-- user avatar -->
            <div
                class="w-[80px] h-[80px] bg-[#D9D9D9] rounded-full flex items-center justify-center overflow-hidden"
            >
                <img
                    v-if="patient.avatarUrl"
                    :src="patient.avatarUrl"
                    class="w-full h-full object-cover"
                />
                <i-solar-user-outline v-else class="text-5xl" />
            </div>

            <!-- user details -->
            <div class="flex flex-col ml-6">
                <p class="text-2xl font-semibold">{{ patient.name }}</p>
                <p
                    class="font-bold flex gap-3"
                    :class="
                        patient.wound.infected === 'Yes'
                            ? 'text-crimson'
                            : 'text-white'
                    "
                >
                    <span>{{
                        patient.wound.infected === "Yes" ? "Critical" : "Stable"
                    }}</span>
                    <span>|</span>
                    <span>{{ patient.wound.type }}</span>
                </p>
            </div>
        </router-link>
    </div>
</template>
