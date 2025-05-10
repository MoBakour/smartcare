<script setup lang="ts">
import { useAuthStore } from "../../stores/auth.store";
import { computed } from "vue";
const authStore = useAuthStore();

const username = computed(() => {
    return authStore.user?.username.split(" ")[0];
});
</script>

<template>
    <header class="w-full py-5 mb-5 flex justify-between items-center">
        <!-- search -->
        <div class="flex items-center gap-1">
            <i-lets-icons-search-light class="text-2xl" />
            <input
                type="text"
                placeholder="Search Patients Here..."
                class="rounded-md px-2 py-1 outline-none"
            />
        </div>

        <!-- user -->
        <div class="flex items-center gap-4">
            <p class="text-lg">
                <span>Dr. </span>
                <span>{{ username }}</span>
            </p>
            <div
                class="w-[40px] h-[40px] bg-[#D9D9D9] rounded-full flex items-center justify-center"
            >
                <i-solar-user-outline class="text-2xl" />
            </div>
        </div>
    </header>
</template>
