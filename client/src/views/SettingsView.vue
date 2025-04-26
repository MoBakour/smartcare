<script setup lang="ts">
import { ref } from "vue";

const name = ref("Mohamed Bakour");
const email = ref("mo.bakour@outlook.com");
const password = ref("");

const handleSave = () => {
    console.log("Saving changes:", {
        name: name.value,
        email: email.value,
        password: password.value,
    });
};

const handleClearData = () => {
    console.log("Clearing all patient data...");
};

const handleDeleteAccount = () => {
    console.log("Deleting account...");
};
</script>

<template>
    <div class="flex flex-col">
        <!-- page title -->
        <h1 class="flex items-center gap-2">
            <span class="text-2xl">Settings</span>
            <i-solar-arrow-right-outline class="text-2xl pt-1" />
        </h1>

        <!-- form section -->
        <form
            @submit.prevent="handleSave"
            class="flex flex-col flex-1 mt-10 mx-auto"
        >
            <div class="w-fit">
                <div class="flex items-start gap-10">
                    <!-- avatar -->
                    <div
                        class="w-[120px] h-[120px] bg-[#D9D9D9] rounded-full flex items-center justify-center"
                    >
                        <i-solar-user-outline class="text-5xl" />
                    </div>

                    <!-- inputs -->
                    <div class="flex flex-col gap-4">
                        <input
                            v-model="name"
                            type="text"
                            placeholder="Name"
                            class="rounded-md px-3 py-1.5 bg-white outline-none text-sm w-[250px]"
                        />
                        <input
                            v-model="email"
                            type="email"
                            placeholder="Email"
                            class="rounded-md px-3 py-1.5 bg-white outline-none text-sm w-[250px]"
                        />
                        <input
                            v-model="password"
                            type="password"
                            placeholder="Password"
                            class="rounded-md px-3 py-1.5 bg-white outline-none text-sm w-[250px]"
                        />

                        <!-- save button -->
                        <div class="flex justify-end">
                            <button
                                type="submit"
                                class="mt-2 w-[200px] bg-theme transition hover:opacity-80 px-6 py-2 text-white font-bold rounded-lg text-sm cursor-pointer disabled:opacity-50"
                                :disabled="!name || !email"
                            >
                                Save Changes
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </form>

        <!-- critical settings -->
        <div class="mt-12 flex flex-col gap-8 mx-auto w-full">
            <h2 class="text-crimson text-xl font-bold">Critical Settings</h2>

            <!-- clear patient data -->
            <div class="flex justify-between items-center">
                <div class="flex flex-col">
                    <p class="font-bold">Clear Patient Data</p>
                    <p class="text-sm text-gray-600">
                        Delete all data related to all patients recorded on the
                        system.
                    </p>
                </div>
                <button
                    @click="handleClearData"
                    class="w-[180px] bg-crimson text-white font-semibold text-sm px-6 py-2 rounded-lg hover:opacity-80 transition cursor-pointer"
                >
                    Clear Data
                </button>
            </div>

            <!-- delete account -->
            <div class="flex justify-between items-center">
                <div class="flex flex-col">
                    <p class="font-bold">Delete Account</p>
                    <p class="text-sm text-gray-600">
                        Delete your account and all associated data, including
                        all patient data.
                    </p>
                </div>
                <button
                    @click="handleDeleteAccount"
                    class="w-[180px] bg-crimson text-white font-semibold text-sm px-6 py-2 rounded-lg hover:opacity-80 transition cursor-pointer"
                >
                    Delete Account
                </button>
            </div>
        </div>
    </div>
</template>
