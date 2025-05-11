<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{ patient: IPatient }>();

const avatarUrl = computed(() => {
    if (!props.patient.avatar) return null;

    return `${import.meta.env.VITE_API_URL}/patient/avatar/${
        props.patient._id
    }`;
});
</script>

<template>
    <div class="flex items-center gap-6">
        <div
            class="w-[100px] h-[100px] bg-[#D9D9D9] rounded-full flex items-center justify-center overflow-hidden"
        >
            <img
                v-if="avatarUrl"
                :src="avatarUrl"
                class="w-full h-full object-cover"
            />
            <i-solar-user-outline v-else class="text-6xl" />
        </div>
        <div class="flex flex-col gap-1">
            <p class="text-gray-400 text-sm">#{{ patient._id }}</p>
            <p class="text-3xl font-bold">{{ patient.name }}</p>

            <div>
                <p class="flex gap-3 font-medium">
                    <span
                        >{{ patient.wound.severity }}
                        {{ patient.wound.type }}</span
                    >
                    <span>|</span>
                    <span>{{ patient.wound.location }}</span>
                </p>
                <p
                    class="font-bold"
                    :class="
                        patient.wound.infected ? 'text-crimson' : 'text-theme'
                    "
                >
                    {{ patient.wound.infected ? `Critical` : `Stable` }}
                    Condition
                </p>
            </div>
        </div>
    </div>
</template>
