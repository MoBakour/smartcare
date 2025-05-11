<script setup lang="ts">
import { Doughnut } from "vue-chartjs";
import { computed } from "vue";

const props = defineProps<{
    percentage: number;
    label: string;
}>();

// Color mapping based on percentage ranges
const percentageColorMap = [
    { max: 20, color: "#ef4444" }, // Red - Critical
    { max: 40, color: "#f97316" }, // Orange - Poor
    { max: 60, color: "#eab308" }, // Yellow - Fair
    { max: 80, color: "#22c55e" }, // Green - Good
    { max: 100, color: "#10b981" }, // Emerald - Excellent
];

// Get color based on percentage
const getColorForPercentage = (percentage: number) => {
    const match = percentageColorMap.find((entry) => percentage <= entry.max);
    return match ? match.color : "#10b981"; // Default to excellent color
};

// Make chart data reactive
const chartData = computed(() => ({
    labels: ["Completed", "Remaining"],
    datasets: [
        {
            data: [props.percentage, 100 - props.percentage],
            backgroundColor: [
                getColorForPercentage(props.percentage),
                "#d9d9d9",
            ],
            borderWidth: 0,
            cutout: "70%",
        },
    ],
}));

// options
const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            display: false,
        },
        tooltip: {
            enabled: false,
        },
    },
};
</script>

<template>
    <div>
        <p class="leading-[30px]">{{ props.label }}</p>
        <div class="w-full h-[100px] relative">
            <Doughnut :data="chartData" :options="chartOptions" />
            <p
                class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-xl font-semibold text-gray-500"
            >
                {{ percentage }}%
            </p>
        </div>
    </div>
</template>
