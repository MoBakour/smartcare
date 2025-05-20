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

interface Settings {
    title: string;
    description: string;
    button: string;
    type: "data" | "account";
}

const settings: Record<string, Settings> = {
    data: {
        title: "Clear Patient Data",
        description:
            "Delete all data related to all patients recorded on the system.",
        button: "Clear Data",
        type: "data",
    },
    account: {
        title: "Delete Account",
        description:
            "Delete your account and all associated data, including all patient data.",
        button: "Delete Account",
        type: "account",
    },
};

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

        <div
            v-for="setting in settings"
            class="flex justify-between items-center max-md:flex-col max-md:items-start max-md:gap-4"
        >
            <div class="flex flex-col">
                <p class="font-bold">{{ setting.title }}</p>
                <p class="text-sm text-gray-600">
                    {{ setting.description }}
                </p>
            </div>
            <button
                @click="
                    () => {
                        showPopup = true;
                        popupType = setting.type;
                    }
                "
                class="shadow-xl w-[180px] bg-crimson text-white font-semibold text-sm px-6 py-2 rounded-lg hover:opacity-80 transition cursor-pointer"
            >
                {{ setting.button }}
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
                    :title="
                        popupType === 'data' ? 'Clear Data' : 'Delete Account'
                    "
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
