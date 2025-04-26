<script setup lang="ts">
interface PatientMainInfo {
    id: string;
    name: string;
    severity: string;
    condition: string;
    location: string;
    status: string;
}

defineProps<{ patient: PatientMainInfo }>();
</script>

<template>
    <div class="flex items-center gap-6">
        <div
            class="w-[100px] h-[100px] bg-[#D9D9D9] rounded-full flex items-center justify-center"
        >
            <i-solar-user-outline class="text-6xl" />
        </div>
        <div class="flex flex-col gap-1">
            <p class="text-gray-400 text-sm">#{{ patient.id }}</p>
            <p class="text-3xl font-bold">{{ patient.name }}</p>

            <div>
                <p class="flex gap-3 font-medium">
                    <span>{{ patient.severity }} {{ patient.condition }}</span>
                    <span>|</span>
                    <span>{{ patient.location }}</span>
                </p>
                <p
                    class="font-bold"
                    :class="
                        patient.status === 'Stable'
                            ? 'text-theme'
                            : 'text-crimson'
                    "
                >
                    {{ patient.status }} Condition
                </p>
            </div>
        </div>
    </div>
</template>
