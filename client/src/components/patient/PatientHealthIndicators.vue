<script setup lang="ts">
import Timeline from "../indicators/Timeline.vue";
import Percentage from "../indicators/Percentage.vue";
import Number from "../indicators/Number.vue";
import { computed, ref } from "vue";

interface PatientHealthIndicators {
    woundTemperature: number;
    woundPH: number;
    moistureLevel: number;
    drugRelease: number;
    systemNotes: string;
    expectedTimeToHeal: number;
}

defineProps<{ patient: PatientHealthIndicators }>();

const data = ref({
    woundTemperature: 53,
    woundPH: 2,
    moistureLevel: 68,
    drugRelease: 81,
    systemNotes: "No issues",
    expectedTimeToHeal: 7,
});

const tempColorMap = [
    { max: 28, color: "#0ea5e9" }, // Very cold (hypothermic risk)
    { max: 30, color: "#38bdf8" }, // Cold (light blue)
    { max: 32, color: "#3b82f6" }, // Cool (normal cold healing)
    { max: 34, color: "#22d3ee" }, // Slightly cool
    { max: 36, color: "#22c55e" }, // Normal wound temperature (healthy)
    { max: 37, color: "#4ade80" }, // Optimal healing temperature
    { max: 38, color: "#eab308" }, // Slightly hot (mild inflammation warning)
    { max: 39, color: "#f59e0b" }, // Hot (early infection warning)
    { max: 40, color: "#f97316" }, // High heat (strong infection alert)
];

const phColorMap = [
    { max: 3.5, color: "#0ea5e9" }, // Very acidic
    { max: 4.5, color: "#38bdf8" }, // Acidic
    { max: 5.0, color: "#22d3ee" }, // Slightly acidic
    { max: 5.5, color: "#2dd4bf" }, // Near healthy
    { max: 6.0, color: "#22c55e" }, // Very healthy
    { max: 6.5, color: "#4ade80" }, // Very healthy
    { max: 7.0, color: "#84cc16" }, // Borderline alkaline
    { max: 7.5, color: "#eab308" }, // Mildly alkaline
    { max: 8.0, color: "#f59e0b" }, // Alkaline
    { max: 8.5, color: "#f97316" }, // Strongly alkaline
];

const tempColor = computed(() => {
    const temp = data.value.woundTemperature;
    const match = tempColorMap.find((entry) => temp < entry.max);
    return match ? match.color : "#ef4444"; // Very high temp (severe infection, necrosis risk)
});

const phColor = computed(() => {
    const pH = data.value.woundPH;
    const match = phColorMap.find((entry) => pH < entry.max);
    return match ? match.color : "#ef4444"; // Highly alkaline
});
</script>

<template>
    <div class="grid grid-cols-4 grid-rows-2 gap-y-4 gap-x-8 mt-8">
        <!-- timeline -->
        <Timeline class="col-span-3 flex flex-col items-start gap-2" />

        <!-- temperature -->
        <Number
            class="col-start-4 flex flex-col items-center gap-2"
            :label="`Wound Temperature`"
            :num="53"
            :temp="true"
            :unit="`°C`"
            :color="tempColor"
        />

        <!-- healing -->
        <Percentage
            class="row-start-2 flex flex-col items-center gap-2"
            :label="`Healing Process %`"
            :percentage="72"
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

        <!-- ph -->
        <Number
            class="row-start-2 flex flex-col items-center gap-2"
            :label="`Wound pH`"
            :num="2"
            :unit="`pH`"
            :color="phColor"
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
