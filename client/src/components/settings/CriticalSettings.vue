<script setup lang="ts">
import { ref } from "vue";
import { useAxios } from "../../composables/useAxios";
import { toast } from "vue3-toastify";
import { useRouter } from "vue-router";
import { useAuthStore } from "../../stores/auth.store";

const router = useRouter();
const authStore = useAuthStore();

const {
    request: requestClearData,
    isLoading: isLoadingClearData,
    error: errorClearData,
} = useAxios();
const {
    request: requestDeleteAccount,
    isLoading: isLoadingDeleteAccount,
    error: errorDeleteAccount,
} = useAxios();

const showPopup = ref(false);
const popupType = ref<"data" | "account">("data");

const handleClearData = async () => {
    await requestClearData("/patient/deleteall", "DELETE");

    showPopup.value = false;

    if (errorClearData.value) {
        toast.error(errorClearData.value);
    } else {
        toast.success("All patient data has been cleared");
    }
};

const handleDeleteAccount = async () => {
    await requestDeleteAccount("/user/delete", "DELETE");

    showPopup.value = false;

    if (errorDeleteAccount.value) {
        toast.error(errorDeleteAccount.value);
    } else {
        toast.success("Account deleted successfully", {
            autoClose: 1000,
            onClose: () => {
                authStore.logout();
                router.push("/auth");
            },
        });
    }
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
                @click="
                    () => {
                        showPopup = true;
                        popupType = 'data';
                    }
                "
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
                @click="
                    () => {
                        showPopup = true;
                        popupType = 'account';
                    }
                "
                class="shadow-xl w-[180px] bg-crimson text-white font-semibold text-sm px-6 py-2 rounded-lg hover:opacity-80 transition cursor-pointer"
            >
                Delete Account
            </button>
        </div>
    </div>

    <!-- confirmation -->
    <div
        class="fixed inset-0 flex items-center justify-center bg-black/70 z-10 transition-all"
        :class="{ 'opacity-0 pointer-events-none': !showPopup }"
    >
        <div
            class="relative bg-white p-5 rounded-lg w-[300px] overflow-hidden flex flex-col"
        >
            <!-- loader -->
            <div
                v-if="isLoadingClearData || isLoadingDeleteAccount"
                class="absolute inset-0 flex items-center justify-center w-full flex-1 bg-white/70 z-100"
            >
                <i-mdi-loading class="animate-spin text-2xl" />
            </div>

            <p class="text-center">
                Are you sure you want to
                {{
                    popupType === "data"
                        ? "clear patient data"
                        : "delete your account"
                }}?
            </p>
            <div class="flex flex-col gap-2 mt-5">
                <button
                    class="bg-crimson text-white font-bold w-full h-[30px] text-sm rounded-md flex items-center justify-center cursor-pointer hover:opacity-80 transition"
                    @click="
                        popupType === 'data'
                            ? handleClearData()
                            : handleDeleteAccount()
                    "
                    title="Clear Data"
                >
                    {{ popupType === "data" ? "Clear Data" : "Delete Account" }}
                </button>
                <button
                    class="bg-gray-300 text-gray-700 w-full h-[30px] text-sm rounded-md cursor-pointer hover:opacity-80 transition"
                    @click="showPopup = false"
                    title="Cancel"
                >
                    Cancel
                </button>
            </div>
        </div>
    </div>
</template>
