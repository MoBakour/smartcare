<script setup lang="ts">
import { Line } from "vue-chartjs";
import { useCommonStore } from "../../stores/common";

const commonStore = useCommonStore();

// colors
const colors: Record<string, string> = {
    Stable: "#50e3c2",
    Critical: "#DC143C",
};

// fake x and y data for the chart
const xData = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
const yData = [0, 0.3, 0.4, 0.6, 0.5, 0.5, 0.7, 0.6, 0.4, 0.3];

const chartData = {
    labels: xData,
    datasets: [
        {
            label: "Health Confidence",
            data: yData,
            borderColor: colors[commonStore.patientStatus],
            backgroundColor: colors[commonStore.patientStatus],
            fill: false,
            tension: 0,
        },
    ],
};

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            display: false,
        },
        title: {
            display: false,
        },
    },
};
</script>

<template>
    <div>
        <p class="text-xl font-semibold leading-[30px]">
            Health Status Timeline
        </p>
        <div class="w-full h-[100px]">
            <Line :data="chartData" :options="chartOptions" />
        </div>
    </div>
</template>
