<script setup lang="ts">
import { ref } from "vue";

const name = ref("");
const sex = ref("");
const age = ref<number | null>(null);
const bed = ref("");
const department = ref("");
const woundType = ref("");
const bloodType = ref("");

const handleSubmit = () => {
    console.log("Submit patient:", {
        name: name.value,
        sex: sex.value,
        age: age.value,
        bed: bed.value,
        department: department.value,
        woundType: woundType.value,
        bloodType: bloodType.value,
    });
};
</script>

<template>
    <div class="flex flex-col">
        <!-- page title -->
        <h1 class="flex items-center gap-2">
            <span class="text-2xl">Add Patient</span>
            <i-solar-arrow-right-outline class="text-2xl pt-1" />
        </h1>

        <!-- form -->
        <form
            @submit.prevent="handleSubmit"
            class="flex flex-col flex-1 mt-10 mx-auto"
        >
            <!-- form layout -->
            <div class="w-fit">
                <div class="flex items-start gap-10">
                    <!-- avatar -->
                    <div
                        class="w-[120px] h-[120px] bg-[#D9D9D9] rounded-full flex items-center justify-center"
                    >
                        <i-solar-user-outline class="text-5xl" />
                    </div>

                    <!-- personal + medical info sections -->
                    <div class="flex justify-between gap-10">
                        <!-- personal info -->
                        <div class="flex flex-col gap-4">
                            <h2 class="text-gray-500 text-md font-semibold">
                                Personal Information
                            </h2>

                            <div class="flex flex-col gap-1">
                                <label for="name" class="text-gray-600 text-sm"
                                    >Patient Name</label
                                >
                                <input
                                    id="name"
                                    v-model="name"
                                    type="text"
                                    placeholder="Enter name"
                                    class="rounded-md px-3 py-1.5 bg-white outline-none text-sm"
                                />
                            </div>

                            <div class="flex justify-between">
                                <button
                                    type="button"
                                    class="w-[80px] py-1.5 rounded-md text-white font-semibold text-sm transition hover:opacity-80 cursor-pointer"
                                    :class="
                                        sex === 'Male'
                                            ? 'bg-blue-400'
                                            : 'bg-gray-300 text-black'
                                    "
                                    @click="sex = 'Male'"
                                >
                                    Male
                                </button>
                                <button
                                    type="button"
                                    class="w-[80px] py-1.5 rounded-md text-white font-semibold text-sm transition hover:opacity-80 cursor-pointer"
                                    :class="
                                        sex === 'Female'
                                            ? 'bg-pink-300'
                                            : 'bg-gray-300 text-black'
                                    "
                                    @click="sex = 'Female'"
                                >
                                    Female
                                </button>
                            </div>

                            <div class="flex justify-between">
                                <div class="flex flex-col gap-1">
                                    <label
                                        for="age"
                                        class="text-gray-600 text-sm"
                                        >Age</label
                                    >
                                    <input
                                        id="age"
                                        v-model="age"
                                        type="number"
                                        placeholder="Age"
                                        class="rounded-md py-1.5 pl-3 bg-white outline-none w-[80px] text-sm"
                                    />
                                </div>
                                <div class="flex flex-col gap-1">
                                    <label
                                        for="bed"
                                        class="text-gray-600 text-sm"
                                        >Bed</label
                                    >
                                    <div class="relative">
                                        <span
                                            class="text-gray-400 absolute top-1/2 left-2 -translate-y-1/2"
                                            >#</span
                                        >
                                        <input
                                            id="bed"
                                            v-model="bed"
                                            type="number"
                                            placeholder="Bed"
                                            class="rounded-md py-1.5 pl-6 bg-white outline-none w-[80px] text-sm"
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- border -->
                        <div
                            class="w-[2px] h-[240px] rounded-4xl bg-gray-300"
                        />

                        <!-- medical info -->
                        <div class="flex flex-col gap-4">
                            <h2 class="text-gray-500 text-md font-semibold">
                                Medical Information
                            </h2>

                            <div class="flex flex-col gap-1">
                                <label
                                    for="department"
                                    class="text-gray-600 text-sm"
                                    >Department</label
                                >
                                <select
                                    id="department"
                                    v-model="department"
                                    class="rounded-md px-3 py-1.5 bg-white outline-none text-sm"
                                >
                                    <option value="" disabled>Select</option>
                                    <option>Cardiology</option>
                                    <option>Neurology</option>
                                    <option>Orthopedics</option>
                                    <option>Emergency</option>
                                </select>
                            </div>

                            <div class="flex flex-col gap-1">
                                <label
                                    for="woundType"
                                    class="text-gray-600 text-sm"
                                    >Wound Type</label
                                >
                                <select
                                    id="woundType"
                                    v-model="woundType"
                                    class="rounded-md px-3 py-1.5 bg-white outline-none text-sm"
                                >
                                    <option value="" disabled>Select</option>
                                    <option>Burns</option>
                                    <option>Fracture</option>
                                    <option>Ulcer</option>
                                    <option>Cut</option>
                                </select>
                            </div>

                            <div class="flex flex-col gap-1">
                                <label
                                    for="bloodType"
                                    class="text-gray-600 text-sm"
                                    >Blood Type</label
                                >
                                <select
                                    id="bloodType"
                                    v-model="bloodType"
                                    class="rounded-md px-3 py-1.5 bg-white outline-none text-sm"
                                >
                                    <option value="" disabled>Select</option>
                                    <option>O-</option>
                                    <option>O+</option>
                                    <option>A-</option>
                                    <option>A+</option>
                                    <option>B-</option>
                                    <option>B+</option>
                                    <option>AB-</option>
                                    <option>AB+</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- submit button -->
                <div class="flex justify-end mt-12">
                    <button
                        type="submit"
                        class="bg-theme hover:opacity-80 transition px-8 py-2 text-white font-bold rounded-lg text-sm cursor-pointer"
                    >
                        Add Patient
                    </button>
                </div>
            </div>
        </form>
    </div>
</template>
