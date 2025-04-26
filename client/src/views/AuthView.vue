<script setup lang="ts">
import { ref } from "vue";

const showPassword = ref(false);
const togglePasswordVisibility = () => {
    showPassword.value = !showPassword.value;
};

const handleSubmit = (event: Event) => {
    const formData = new FormData(event.target as HTMLFormElement);
    const username = formData.get("username") as string;
    const password = formData.get("password") as string;

    // Perform login logic here
    console.log("Username:", username);
    console.log("Password:", password);
};
</script>

<template>
    <div>
        <!-- squares -->
        <div>
            <div
                class="w-[500px] h-[500px] bg-theme rounded-[80px] rotate-45 opacity-50 fixed top-0 -translate-x-1/3 -translate-y-1/8 pointer-events-none"
            />
            <div
                class="w-[500px] h-[500px] bg-theme rounded-[80px] rotate-45 fixed bottom-0 -translate-x-1/8 translate-y-1/3 pointer-events-none"
            >
                <!-- logo -->
                <img
                    src="../assets/images/logo.png"
                    alt="logo"
                    class="-rotate-45 opacity-60 w-[450px] relative -bottom-[25px]"
                />
            </div>
            <div
                class="w-[500px] h-[500px] bg-theme rounded-[80px] opacity-30 blur-3xl rotate-45 fixed right-0 translate-x-1/3 -translate-y-1/8 pointer-events-none"
            />
        </div>

        <!-- form -->
        <form
            @submit.prevent="handleSubmit"
            class="fixed right-0 w-3/5 flex flex-col items-center justify-center gap-5 h-screen"
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
                <!-- username input -->
                <input
                    type="text"
                    name="username"
                    placeholder="Username"
                    class="bg-white w-[260px] px-2 py-1 rounded-md outline-none"
                />

                <!-- password input -->
                <div class="relative">
                    <input
                        :type="showPassword ? 'text' : 'password'"
                        name="password"
                        placeholder="Password"
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
            </div>

            <!-- submit button -->
            <button
                type="submit"
                class="group bg-theme text-white text-lg font-bold w-[260px] py-1 rounded-md hover:opacity-80 cursor-pointer transition flex items-center justify-center gap-1"
            >
                <span>Login</span>
                <i-flowbite-arrow-right-outline
                    class="text-xl group-hover:translate-x-1 transition"
                />
            </button>
        </form>
    </div>
</template>
