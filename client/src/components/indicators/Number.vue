<script lang="ts" setup>
const { label, num, unit, color } = defineProps<{
    label: string;
    num: number;
    unit: string;
    color: string;
}>();
</script>

<template>
    <div>
        <p class="leading-[30px]">{{ label }}</p>
        <p
            class="w-full h-[100px] flex items-center justify-center text-7xl font-bold"
            :style="{ color: color }"
        >
            {{ num }} <span class="text-3xl pl-3 pb-6">{{ unit }}</span>
        </p>
    </div>
</template>
