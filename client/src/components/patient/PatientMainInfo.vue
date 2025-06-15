<script setup lang="ts">
import { computed } from "vue";
import { useCommonStore } from "../../stores/common.store";

const commonStore = useCommonStore();

const props = defineProps<{ patient: IPatient }>();

const avatarUrl = computed(() => {
    if (!props.patient.avatar) return null;

    return `${import.meta.env.VITE_API_URL}/patient/avatar/${
        props.patient._id
    }`;
});

const isCritical = computed(() => {
    return commonStore.patientStatus === "Critical";
});
</script>

<template>
    <div class="flex items-center gap-6 max-md:gap-3">
        <div
            class="w-[100px] h-[100px] min-w-[100px] max-md:w-[80px] max-md:h-[80px] max-md:min-w-[80px] bg-[#D9D9D9] rounded-full flex items-center justify-center overflow-hidden"
        >
            <img
                v-if="avatarUrl"
                :src="avatarUrl"
                onerror="this.src='/avatar.jpg'"
                class="w-full h-full object-cover"
            />
            <i-solar-user-outline v-else class="text-6xl max-md:text-4xl" />
        </div>
        <div class="flex flex-col gap-1 max-md:gap-0.25">
            <p class="text-gray-400 text-sm max-md:text-xs">
                #{{ patient._id }}
            </p>
            <p class="text-3xl max-md:text-xl font-bold">{{ patient.name }}</p>

            <div class="max-md:text-sm">
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
                    :class="isCritical ? 'text-crimson' : 'text-theme'"
                >
                    {{ isCritical ? `Critical` : `Stable` }}
                    Condition
                </p>
            </div>
        </div>
    </div>
</template>
