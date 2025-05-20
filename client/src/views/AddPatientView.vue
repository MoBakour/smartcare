<script setup lang="ts">
import { ref } from "vue";
import PersonalInputs from "../components/add/PersonalInputs.vue";
import MedicalInputs from "../components/add/MedicalInputs.vue";
import { useAxios } from "../composables/useAxios";
import { useRouter } from "vue-router";

const { request, isLoading, error } = useAxios();
const router = useRouter();

const patientData = ref({
    avatarFile: null,
    avatarPreview: null,
    name: "",
    gender: "",
    age: "",
    bed: "",
    department: "",
    bloodType: "",
    wound: {
        type: "",
        location: "",
        severity: "",
        infected: "",
        size: "",
        treatment: "",
    },
});

const handleSubmit = async () => {
    const formData = new FormData();

    formData.append("avatar", patientData.value.avatarFile || "");
    formData.append("name", patientData.value.name);
    formData.append("gender", patientData.value.gender);
    formData.append("age", patientData.value.age);
    formData.append("bed", patientData.value.bed);
    formData.append("department", patientData.value.department);
    formData.append("blood_type", patientData.value.bloodType);
    formData.append("wound", JSON.stringify(patientData.value.wound));

    const res = await request("/patient/new", "POST", formData);

    if (res) {
        router.push(`/patients/${res.patient._id}?new=true`);
    }
};
</script>

<template>
    <div class="flex flex-col mb-10">
        <!-- page title -->
        <h1 class="flex items-center gap-2">
            <span class="text-2xl">Add Patient</span>
            <i-solar-arrow-right-outline class="text-2xl pt-1" />
        </h1>

        <!-- form -->
        <form
            @submit.prevent="handleSubmit"
            class="flex flex-col flex-1 mt-10 max-md:mt-5 mx-auto"
        >
            <!-- error message -->
            <div
                v-if="error"
                class="bg-crimson/10 text-crimson text-sm rounded-md p-2 mb-3"
            >
                {{ error }}
            </div>

            <!-- personal + medical info sections -->
            <div
                class="flex justify-between items-start gap-10 max-md:flex-col max-md:items-center max-md:gap-5"
            >
                <!-- personal info -->
                <PersonalInputs v-model="patientData" />

                <!-- medical info -->
                <MedicalInputs
                    v-model="patientData"
                    class="border-l-2 border-gray-300 pl-10 max-md:border-l-0 max-md:border-t-2 max-md:pl-0 max-md:pt-5"
                />
            </div>

            <!-- submit button -->
            <div class="flex justify-end mt-8">
                <button
                    type="submit"
                    class="bg-theme hover:opacity-80 transition w-[140px] h-[40px] text-white font-bold rounded-md text-sm cursor-pointer flex items-center justify-center disabled:opacity-50 disabled:cursor-default"
                    :disabled="isLoading"
                    @click="handleSubmit"
                >
                    <span v-if="!isLoading">Add Patient</span>
                    <i-line-md:loading-twotone-loop v-else class="text-xl" />
                </button>
            </div>
        </form>
    </div>
</template>
