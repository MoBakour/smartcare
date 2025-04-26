<script setup lang="ts">
interface PatientDetails {
    sex: string;
    age: number;
    blood: string;
    bed: string;
    department: string;
    checkIn: string;
}

defineProps<{ patient: PatientDetails }>();
</script>
<template>
    <div class="flex gap-10">
        <div class="flex gap-3">
            <div class="flex flex-col text-gray-500">
                <span>Sex: </span>
                <span>Age: </span>
                <span>Blood: </span>
            </div>

            <div class="flex flex-col font-semibold">
                <span>{{ patient.sex }}</span>
                <span>{{ patient.age }}</span>
                <span>{{ patient.blood }}</span>
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
                <span>{{ patient.checkIn }}</span>
            </div>
        </div>
    </div>
</template>
