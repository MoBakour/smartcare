<script setup lang="ts">
interface PatientHealthIndicators {
    woundTemperature: number;
    woundPH: number;
    moistureLevel: number;
    drugRelease: number;
    systemNotes: string;
    expectedTimeToHeal: number;
}

defineProps<{ patient: PatientHealthIndicators }>();
</script>

<template>
    <!-- timeline -->
    <div class="mt-8">
        <p class="text-xl font-semibold mb-2">Timeline</p>
        <div class="w-full h-[80px] bg-theme/20 rounded-2xl"></div>
    </div>

    <!-- health indicators -->
    <div class="flex justify-between items-center gap-6 mt-8">
        <div class="flex flex-col items-center gap-2">
            <p>Wound Temperature</p>
            <div class="w-[120px] h-[60px] bg-[#FAD8C6] rounded-2xl"></div>
        </div>
        <div class="flex flex-col items-center gap-2">
            <p>Wound pH</p>
            <div class="w-[120px] h-[60px] bg-[#F0F9CC] rounded-2xl"></div>
        </div>
        <div class="flex flex-col items-center gap-2">
            <p>Moisture Level %</p>
            <div class="w-[120px] h-[60px] bg-[#C5E9F5] rounded-2xl"></div>
        </div>
        <div class="flex flex-col items-center gap-2">
            <p>Drug Release %</p>
            <div class="w-[120px] h-[60px] bg-[#DAF5CB] rounded-2xl"></div>
        </div>
    </div>

    <!-- system notes -->
    <div class="mt-4">
        <p class="text-gray-500 text-sm font-semibold">System —</p>
        <p class="text-lg">
            {{ patient.systemNotes }}
        </p>
        <p class="text-gray-500">
            Expected time to heal — {{ patient.expectedTimeToHeal }} days
        </p>
    </div>
</template>
