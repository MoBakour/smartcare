<script setup lang="ts">
const handleClearData = () => {
    console.log("Clearing all patient data...");
};

const handleDeleteAccount = () => {
    console.log("Deleting account...");
};
</script>

<template>
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
                class="shadow-xl w-[180px] bg-crimson text-white font-semibold text-sm px-6 py-2 rounded-lg hover:opacity-80 transition cursor-pointer"
            >
                Clear Data
            </button>
        </div>

        <!-- delete account -->
        <div class="flex justify-between items-center">
            <div class="flex flex-col">
                <p class="font-bold">Delete Account</p>
                <p class="text-sm text-gray-600">
                    Delete your account and all associated data, including all
                    patient data.
                </p>
            </div>
            <button
                @click="handleDeleteAccount"
                class="shadow-xl w-[180px] bg-crimson text-white font-semibold text-sm px-6 py-2 rounded-lg hover:opacity-80 transition cursor-pointer"
            >
                Delete Account
            </button>
        </div>
    </div>
</template>
