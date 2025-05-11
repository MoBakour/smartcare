<script setup lang="ts">
import Timeline from "../indicators/Timeline.vue";
import Percentage from "../indicators/Percentage.vue";
import Number from "../indicators/Number.vue";
import { computed, ref, watch } from "vue";

interface PatientHealthIndicators {
    "Wound Temperature": number;
    "Wound pH": number;
    "Moisture Level": number;
    "Drug Release": number;
    "Healing Time": number;
}

const props = defineProps<{ data: PatientHealthIndicators }>();

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

const healingColorMap = [
    { max: 10, color: "#0ea5e9" }, // Very cold (hypothermic risk)
    { max: 20, color: "#38bdf8" }, // Cold (light blue)
    { max: 30, color: "#3b82f6" }, // Cool (normal cold healing)
    { max: 40, color: "#22d3ee" }, // Slightly cool
];

const tempColor = computed(() => {
    const temp = props.data["Wound Temperature"];
    const match = tempColorMap.find((entry) => temp < entry.max);
    return match ? match.color : "#ef4444";
});

const phColor = computed(() => {
    const pH = props.data["Wound pH"];
    const match = phColorMap.find((entry) => pH < entry.max);
    return match ? match.color : "#ef4444";
});

const healingColor = computed(() => {
    const healingTime = props.data["Healing Time"];
    const match = healingColorMap.find((entry) => healingTime < entry.max);
    return match ? match.color : "#ef4444";
});

watch(props.data, (newData) => {
    console.log(props.data);
});
</script>

<template>
    <div class="grid grid-cols-4 grid-rows-2 gap-y-4 gap-x-8 mt-8">
        <!-- timeline -->
        <Timeline class="col-span-3 flex flex-col items-start gap-2" />

        <!-- temperature -->
        <Number
            class="row-start-2 flex flex-col items-center gap-2"
            :label="`Wound Temperature`"
            :num="props.data['Wound Temperature']"
            :temp="true"
            :unit="`°C`"
            :color="tempColor"
        />

        <!-- ph -->
        <Number
            class="row-start-2 flex flex-col items-center gap-2"
            :label="`Wound pH`"
            :num="props.data['Wound pH']"
            :unit="`pH`"
            :color="phColor"
        />

        <!-- healing -->
        <Number
            class="row-start-2 flex flex-col items-center gap-2"
            :label="`Time to Heal`"
            :num="Math.round(props.data['Healing Time'])"
            :unit="`days`"
            :color="healingColor"
        />

        <!-- moisture -->
        <Percentage
            class="col-start-4 flex flex-col items-center gap-2"
            :label="`Moisture Level %`"
            :percentage="props.data['Moisture Level']"
        />

        <!-- drug -->
        <Percentage
            class="col-start-4 flex flex-col items-center gap-2"
            :label="`Drug Release %`"
            :percentage="props.data['Drug Release']"
        />
    </div>
</template>
