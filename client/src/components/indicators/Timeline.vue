<script setup lang="ts">
import { ref, computed } from "vue";
import { Line } from "vue-chartjs";
import { useCommonStore } from "../../stores/common.store";

const commonStore = useCommonStore();

const props = defineProps<{ data: PatientHealthIndicators[] }>();

const activeIndicator = ref("Wound Temperature");

// colors
const colors: Record<string, string> = {
    "Wound Temperature": "#f97316",
    "Wound pH": "#3b82f6",
    "Drug Release": "#22c55e",
    "Moisture Level": "#8b5cf6",
};

// chart data
const xData = computed(() => {
    return props.data.map((item) => item["Time"]);
});
const yData = computed(() => {
    return props.data.map((item) => item[activeIndicator.value]);
});

const chartData = computed(() => {
    return {
        labels: xData.value,
        datasets: [
            {
                label: activeIndicator.value,
                data: yData.value,
                borderColor: colors[activeIndicator.value],
                backgroundColor: colors[activeIndicator.value],
                fill: false,
                tension: 0,
            },
        ],
    };
});

// chart options
const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
        x: {
            ticks: {
                autoSkip: true,
                maxTicksLimit: 10,
                maxRotation: 0,
                minRotation: 0,
            },
        },
    },
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
        <div class="flex items-center w-full justify-between">
            <p class="text-xl font-semibold leading-[30px]">
                Health Status Timeline
            </p>

            <!-- switches -->
            <div class="flex items-center gap-2">
                <button
                    class="px-2 py-1 rounded-sm text-xs bg-[#f97316] text-white hover:bg-[#f97316]/80 transition-all cursor-pointer"
                    @click="activeIndicator = 'Wound Temperature'"
                >
                    Temperature
                </button>
                <button
                    class="px-2 py-1 rounded-sm text-xs bg-[#3b82f6] text-white hover:bg-[#3b82f6]/80 transition-all cursor-pointer"
                    @click="activeIndicator = 'Wound pH'"
                >
                    pH
                </button>
                <button
                    class="px-2 py-1 rounded-sm text-xs bg-[#22c55e] text-white hover:bg-[#22c55e]/80 transition-all cursor-pointer"
                    @click="activeIndicator = 'Drug Release'"
                >
                    Drug Release
                </button>
                <button
                    class="px-2 py-1 rounded-sm text-xs bg-[#8b5cf6] text-white hover:bg-[#8b5cf6]/80 transition-all cursor-pointer"
                    @click="activeIndicator = 'Moisture Level'"
                >
                    Moisture Level
                </button>
            </div>
        </div>
        <div class="w-full h-[100px]">
            <Line :data="chartData" :options="chartOptions" />
        </div>
    </div>
</template>
