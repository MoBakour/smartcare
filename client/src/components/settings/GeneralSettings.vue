<script setup lang="ts">
import { ref } from "vue";

const name = ref("Mohamed Bakour");
const email = ref("mo.bakour@outlook.com");
const password = ref("");

const avatarPreview = ref<string | null>(null);
const avatarFile = ref<File | null>(null);

const handleFileChange = (event: Event) => {
    const target = event.target as HTMLInputElement;
    const file = target.files?.[0];

    if (file) {
        avatarFile.value = file;

        const reader = new FileReader();
        reader.onload = () => {
            avatarPreview.value = reader.result as string;
        };
        reader.readAsDataURL(file);
    }
};

const handleSave = () => {
    console.log("Saving changes:", {
        name: name.value,
        email: email.value,
        password: password.value,
        avatar: avatarPreview.value,
    });
};
</script>

<template>
    <!-- form section -->
    <form
        @submit.prevent="handleSave"
        class="flex flex-col flex-1 mt-10 mx-auto"
    >
        <div class="w-fit">
            <div class="flex items-start gap-10">
                <!-- avatar -->
                <label
                    for="avatar"
                    class="shadow-lg w-[120px] h-[120px] bg-[#D9D9D9] rounded-full flex items-center justify-center overflow-hidden cursor-pointer hover:opacity-80 transition"
                >
                    <template v-if="avatarPreview">
                        <img
                            :src="avatarPreview"
                            alt="Profile Preview"
                            class="w-full h-full object-cover"
                        />
                    </template>
                    <template v-else>
                        <i-solar-user-outline class="text-5xl" />
                    </template>
                </label>

                <!-- hidden file input -->
                <input
                    id="avatar"
                    type="file"
                    accept="image/*"
                    class="hidden"
                    @change="handleFileChange"
                />

                <!-- inputs -->
                <div class="flex flex-col gap-4">
                    <input
                        v-model="name"
                        type="text"
                        placeholder="Name"
                        class="shadow-md rounded-md px-3 py-1.5 bg-white outline-none text-sm w-[250px]"
                    />
                    <input
                        v-model="email"
                        type="email"
                        placeholder="Email"
                        class="shadow-md rounded-md px-3 py-1.5 bg-white outline-none text-sm w-[250px]"
                    />
                    <input
                        v-model="password"
                        type="password"
                        placeholder="Password"
                        class="shadow-md rounded-md px-3 py-1.5 bg-white outline-none text-sm w-[250px]"
                    />

                    <!-- save button -->
                    <div class="flex justify-end">
                        <button
                            type="submit"
                            class="shadow-md mt-2 w-[200px] bg-theme transition hover:opacity-80 px-6 py-2 text-white font-bold rounded-lg text-sm cursor-pointer disabled:opacity-50"
                            :disabled="!name || !email"
                        >
                            Save Changes
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </form>
</template>
