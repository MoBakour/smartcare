<script setup lang="ts">
import { ref } from "vue";
import { useAuthStore } from "../../stores/auth.store";
import { useAxios } from "../../composables/useAxios";
import { useRouter } from "vue-router";

const showPassword = ref(false);
const togglePasswordVisibility = () => {
    showPassword.value = !showPassword.value;
};

const authStore = useAuthStore();
const { request, isLoading, error } = useAxios();
const router = useRouter();

const handleSubmit = async (event: Event) => {
    const formData = new FormData(event.target as HTMLFormElement);
    const email = formData.get("email") as string;
    const password = formData.get("password") as string;

    const response = await request("/auth/login", "POST", {
        email,
        password,
    });

    if (response) {
        authStore.login(response.token, response.user);
        router.push("/patients");
    }
};

const emit = defineEmits(["switchToSignup"]);
</script>

<template>
    <form
        @submit.prevent="handleSubmit"
        class="flex flex-col items-center justify-center gap-5"
    >
        <!-- user default avatar -->
        <div
            class="w-[120px] h-[120px] bg-[#D9D9D9] rounded-full flex items-center justify-center"
        >
            <i-solar-user-outline class="text-7xl" />
        </div>
        <p class="font-bold text-xl">Healthcare Provider Login</p>

        <!-- inputs -->
        <div class="flex flex-col gap-3">
            <!-- email input -->
            <input
                type="email"
                name="email"
                placeholder="Email"
                required
                class="bg-white w-[260px] px-2 py-1 rounded-md outline-none"
            />

            <!-- password input -->
            <div class="relative">
                <input
                    :type="showPassword ? 'text' : 'password'"
                    name="password"
                    placeholder="Password"
                    required
                    class="bg-white w-[260px] px-2 py-1 rounded-md outline-none"
                />

                <!-- password eye icon -->
                <div
                    class="absolute top-1/2 right-2 -translate-y-1/2 cursor-pointer transition-opacity opacity-50 hover:opacity-100"
                >
                    <i-mdi-eye
                        v-if="!showPassword"
                        @click="togglePasswordVisibility"
                    />

                    <i-mdi-eye-off
                        v-if="showPassword"
                        @click="togglePasswordVisibility"
                    />
                </div>
            </div>

            <!-- error message -->
            <p
                v-if="error"
                class="text-crimson bg-crimson/10 px-2 py-1 rounded-md text-sm text-center"
            >
                {{ error }}
            </p>
        </div>

        <!-- submit button -->
        <button
            type="submit"
            :disabled="isLoading"
            class="group bg-theme text-white text-lg font-bold w-[260px] py-1 rounded-md hover:opacity-80 cursor-pointer transition flex items-center justify-center gap-1 disabled:opacity-50 disabled:cursor-not-allowed"
        >
            <span v-if="!isLoading">Login</span>
            <i-line-md:loading-twotone-loop v-else class="text-2xl" />
            <i-flowbite-arrow-right-outline
                v-if="!isLoading"
                class="text-xl group-hover:translate-x-1 transition"
            />
        </button>

        <!-- signup link -->
        <p class="text-sm text-gray-500">
            No account?
            <button
                type="button"
                @click="emit('switchToSignup')"
                class="text-theme hover:underline transition cursor-pointer"
            >
                Sign up
            </button>
        </p>
    </form>
</template>
