<script setup lang="ts">
import { Doughnut } from "vue-chartjs";

const props = defineProps<{
    percentage: number;
    label: string;
}>();

// colors
const colors = [
    "#50e3c2",
    "#FBBF24",
    "#F472B6",
    "#A78BFA",
    "#F9A8D4",
    "#34D399",
    "#60A5FA",
    "#818CF8",
    "#F87171",
    "#FACC15",
    "#10B981",
    "#3B82F6",
    "#6366F1",
    "#EF4444",
    "#EAB308",
    "#22D3EE",
    "#A3E635",
    "#D946EF",
    "#FB923C",
    "#4ADE80",
];

// data
const chartData = {
    labels: ["Completed", "Remaining"],
    datasets: [
        {
            data: [props.percentage, 100 - props.percentage],
            backgroundColor: [
                colors[Math.floor(Math.random() * colors.length)],
                "#d9d9d9",
            ],
            borderWidth: 0,
            cutout: "70%",
        },
    ],
};

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
