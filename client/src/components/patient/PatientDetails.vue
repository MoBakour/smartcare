<script setup lang="ts">
import { formatDate } from "../../utils/utils";

defineProps<{ patient: IPatient }>();
</script>

<template>
    <div class="flex gap-10 max-md:text-sm max-md:gap-6">
        <div class="flex gap-3">
            <div class="flex flex-col text-gray-500">
                <span>Gender: </span>
                <span>Age: </span>
                <span>Blood: </span>
            </div>

            <div class="flex flex-col font-semibold">
                <span>{{
                    patient.gender[0].toUpperCase() + patient.gender.slice(1)
                }}</span>
                <span>{{ patient.age }}</span>
                <span>{{ patient.blood_type }}</span>
            </div>
        </div>

        <div class="flex gap-3">
            <div class="flex flex-col text-gray-500">
                <span>Bed: </span>
                <span>Dept: </span>
                <span>Check-in: </span>
            </div>

            <div class="flex flex-col font-semibold">
                <span>{{ patient.bed }}</span>
                <span>{{ patient.department }}</span>
                <span>{{ formatDate(new Date(patient.created_at)) }}</span>
            </div>
        </div>
    </div>
</template>
