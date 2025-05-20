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
        <p class="leading-[30px] whitespace-nowrap">{{ label }}</p>
        <p
            class="w-full h-[60px] flex items-center justify-center text-7xl max-xs:text-5xl font-bold"
            :style="{ color: color }"
        >
            {{ num }} <span class="text-3xl pl-3 pb-6">{{ unit }}</span>
        </p>
    </div>
</template>
