<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useAxios } from "../composables/useAxios";

const { request, isLoading, error } = useAxios();
const patients = ref<IPatient[]>([]);

const fetchPatients = async () => {
    const response = await request("/patient/all", "GET");

    if (response) {
        patients.value = response.patients
            .map((patient: IPatient) => {
                return {
                    ...patient,
                    avatar: computed(() => {
                        if (!patient.avatar) return null;

                        return `${
                            import.meta.env.VITE_API_URL
                        }/patient/avatar/${patient._id}`;
                    }),
                };
            })
            .sort((a: IPatient, b: IPatient) => {
                const aSevere = a.wound.severity === "Severe";
                const bSevere = b.wound.severity === "Severe";

                if (aSevere && !bSevere) return -1;
                if (!aSevere && bSevere) return 1;
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
    <div
        v-else
        class="mt-10 mb-15 max-sm:mt-8 max-sm:mb-10 flex flex-col items-center gap-6"
    >
        <router-link
            :to="`/patients/${patient._id}`"
            v-for="patient in patients"
            :key="patient._id"
            class="w-[80%] max-sm:w-[90%] max-xs:w-[98%] p-6 max-sm:p-4 shadow-xl rounded-2xl flex gap-6 max-sm:gap-4 max-xs:gap-2 items-center bg-gradient-to-r transition-all hover:w-[82%] max-sm:hover:w-[92%] max-xs:hover:w-[100%] cursor-pointer"
            :class="
                patient.wound.severity === 'Severe'
                    ? 'from-crimson/35 to-crimson/15'
                    : 'from-theme/45 to-theme/25'
            "
        >
            <!-- user avatar -->
            <div
                class="w-[80px] h-[80px] min-w-[80px] max-sm:w-[70px] max-sm:h-[70px] max-sm:min-w-[70px] max-xs:w-[60px] max-xs:h-[60px] max-xs:min-w-[60px] bg-[#D9D9D9] rounded-full flex items-center justify-center overflow-hidden"
            >
                <img
                    v-if="patient.avatar"
                    :src="patient.avatar"
                    onerror="this.src='/avatar.jpg'"
                    class="w-full h-full object-cover"
                />
                <i-solar-user-outline v-else class="text-5xl" />
            </div>

            <!-- user details -->
            <div class="flex flex-col">
                <p class="text-2xl max-sm:text-xl max-xs:text-lg font-semibold">
                    {{ patient.name }}
                </p>
                <p
                    class="font-bold flex gap-3 max-sm:gap-2 max-sm:text-sm max-xs:text-xs"
                    :class="
                        patient.wound.severity === 'Severe'
                            ? 'text-crimson'
                            : 'text-white'
                    "
                >
                    <span>{{ patient.wound.severity }}</span>
                    <span>|</span>
                    <span>{{ patient.wound.type }}</span>
                </p>
            </div>
        </router-link>
    </div>
</template>
