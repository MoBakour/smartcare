<script setup lang="ts">
import { ref } from "vue";

const patient = ref({
    id: "ff763hjf92",
    name: "Amina Khoury",
    severity: "Moderate",
    condition: "Burn",
    location: "Elbow",
    status: "Stable",
    sex: "Female",
    age: 99,
    blood: "AB-",
    bed: "456",
    department: "Cardiology",
    checkIn: "23/12/25",
    systemNotes:
        "Patient is in stable condition — continue administering medication at the current dosage and interval.",
    expectedTimeToHeal: 7,
});
</script>

<template>
    <div>
        <!-- breadcrumb -->
        <div class="flex items-center gap-2">
            <router-link to="/patients" class="hover:underline"
                >Patients</router-link
            >
            <span>›</span>
            <span class="text-gray-500">{{ patient.name }}</span>
        </div>

        <!-- patient info -->
        <div class="flex items-center justify-between gap-10 mt-6">
            <!-- main info -->
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
                            <span
                                >{{ patient.severity }}
                                {{ patient.condition }}</span
                            >
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

            <!-- details -->
            <div class="flex gap-10">
                <div class="flex gap-3">
                    <div class="flex flex-col text-gray-500">
                        <span>Sex: </span>
                        <span>Age: </span>
                        <span>Blood: </span>
                    </div>

                    <div class="flex flex-col font-semibold">
                        <span>{{ patient.sex }}</span>
                        <span>{{ patient.age }}</span>
                        <span>{{ patient.blood }}</span>
                    </div>
                </div>

                <div class="flex gap-3">
                    <div class="flex flex-col text-gray-500">
                        <span>Bed: </span>
                        <span>Dept: </span>
                        <span>Check-in: </span>
                    </div>

                    <div class="flex flex-col font-semibold">
                        <span>{{ patient.bed }}</span>
                        <span>{{ patient.department }}</span>
                        <span>{{ patient.checkIn }}</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- timeline -->
        <div class="mt-8">
            <p class="text-xl font-semibold mb-2">Timeline</p>
            <div class="w-full h-[80px] bg-theme/20 rounded-2xl"></div>
        </div>

        <!-- health indicators -->
        <div class="flex justify-between items-center gap-6 mt-8">
            <div class="flex flex-col items-center gap-2">
                <p>Wound Temperature</p>
                <div class="w-[120px] h-[60px] bg-[#FAD8C6] rounded-2xl"></div>
            </div>
            <div class="flex flex-col items-center gap-2">
                <p>Wound pH</p>
                <div class="w-[120px] h-[60px] bg-[#F0F9CC] rounded-2xl"></div>
            </div>
            <div class="flex flex-col items-center gap-2">
                <p>Moisture Level %</p>
                <div class="w-[120px] h-[60px] bg-[#C5E9F5] rounded-2xl"></div>
            </div>
            <div class="flex flex-col items-center gap-2">
                <p>Drug Release %</p>
                <div class="w-[120px] h-[60px] bg-[#DAF5CB] rounded-2xl"></div>
            </div>
        </div>

        <!-- system notes -->
        <div class="mt-4">
            <p class="text-gray-500 text-sm font-semibold">System —</p>
            <p class="text-lg">
                {{ patient.systemNotes }}
            </p>
            <p class="text-gray-500">
                Expected time to heal — {{ patient.expectedTimeToHeal }} days
            </p>
        </div>
    </div>
</template>
