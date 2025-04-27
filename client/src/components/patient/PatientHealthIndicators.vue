<script setup lang="ts">
import Timeline from "../indicators/Timeline.vue";

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
    <div class="grid grid-cols-4 grid-rows-2 gap-y-4 gap-x-8 mt-8">
        <!-- timeline -->
        <Timeline class="col-span-3 flex flex-col items-start gap-2" />

        <!-- healing -->
        <Percentage
            class="col-start-4 flex flex-col items-center gap-2"
            :label="`Healing Process %`"
            :percentage="72"
        />

        <!-- temperature -->
        <Percentage
            class="row-start-2 flex flex-col items-center gap-2"
            :label="`Wound Temperature`"
            :percentage="53"
        />

        <!-- ph -->
        <Percentage
            class="row-start-2 flex flex-col items-center gap-2"
            :label="`Wound pH`"
            :percentage="45"
        />

        <!-- moisture -->
        <Percentage
            class="row-start-2 flex flex-col items-center gap-2"
            :label="`Moisture Level %`"
            :percentage="68"
        />

        <!-- drug -->
        <Percentage
            class="row-start-2 flex flex-col items-center gap-2"
            :label="`Drug Release %`"
            :percentage="81"
        />
    </div>

    <!-- system notes -->
    <!-- <div class="mt-4">
        <p class="text-gray-500 text-sm font-semibold">System —</p>
        <p class="text-lg">
            {{ patient.systemNotes }}
        </p>
        <p class="text-gray-500">
            Expected time to heal — {{ patient.expectedTimeToHeal }} days
        </p>
    </div> -->
</template>
