<script setup lang="ts">
import { useAuthStore } from "../../stores/auth.store";
import { useAxios } from "../../composables/useAxios";
import { computed, ref, watch } from "vue";

const authStore = useAuthStore();
const { request } = useAxios();

const username = computed(() => {
    return authStore.user?.username.split(" ")[0];
});

const avatarUrl = computed(() => {
    return `${import.meta.env.VITE_API_URL}/user/avatar/${authStore.user?._id}`;
});

const searchResults = ref<IPatient[]>([]);
const searchQuery = ref("");
const searchTimeout = ref<number | null>(null);
const selectedIndex = ref(-1);

watch(searchQuery, (newVal) => {
    if (searchTimeout.value) clearTimeout(searchTimeout.value);

    searchTimeout.value = setTimeout(async () => {
        const query = newVal.trim();
        if (query.length === 0) {
            searchResults.value = [];
            selectedIndex.value = -1;
            return;
        }

        const data = await request(`/patient/search/${query}`, "GET");

        if (data) {
            searchResults.value = data.patients.map((patient: IPatient) => ({
                ...patient,
                avatar: patient.avatar
                    ? `${import.meta.env.VITE_API_URL}/patient/avatar/${
                          patient._id
                      }`
                    : "",
            }));
            selectedIndex.value = -1;
        }
    }, 200);
});

const handleKeydown = (e: KeyboardEvent) => {
    if (!searchResults.value.length) return;

    if (e.key === "ArrowDown") {
        e.preventDefault();
        selectedIndex.value =
            (selectedIndex.value + 1) % searchResults.value.length;
    } else if (e.key === "ArrowUp") {
        e.preventDefault();
        selectedIndex.value =
            selectedIndex.value <= 0
                ? searchResults.value.length - 1
                : selectedIndex.value - 1;
    } else if (e.key === "Enter" && selectedIndex.value >= 0) {
        e.preventDefault();
        window.location.href = `/patients/${
            searchResults.value[selectedIndex.value]._id
        }`;
    }
};
</script>

<template>
    <header class="w-full py-5 mb-5 flex justify-between items-center">
        <!-- search -->
        <div class="relative flex items-center gap-1 z-5">
            <i-lets-icons-search-light class="text-2xl" />
            <input
                type="text"
                v-model="searchQuery"
                placeholder="Search Patients Here..."
                class="rounded-md px-2 py-1 outline-none"
                @keydown="handleKeydown"
            />

            <!-- search results -->
            <div
                v-if="searchResults.length > 0"
                class="absolute -bottom-2 left-0 translate-y-full w-full p-2 bg-white shadow-lg rounded-md flex flex-col gap-1"
            >
                <a
                    v-for="(patient, index) in searchResults"
                    :href="`/patients/${patient._id}`"
                    :key="patient._id"
                    :class="[
                        'flex items-center gap-2 p-2 rounded-md hover:bg-gray-100',
                        index === selectedIndex ? 'bg-gray-100' : '',
                    ]"
                >
                    <div
                        class="w-8 h-8 rounded-full bg-[#D9D9D9] flex items-center justify-center overflow-hidden"
                    >
                        <img
                            v-if="patient.avatar"
                            :src="patient.avatar"
                            alt="avatar"
                            class="w-full h-full object-cover"
                        />
                        <i-solar-user-outline v-else class="text-xl" />
                    </div>
                    <p>{{ patient.name }}</p>
                </a>
            </div>
        </div>

        <!-- user -->
        <div class="flex items-center gap-4">
            <p class="text-lg">
                <span>Dr. </span>
                <span>{{ username }}</span>
            </p>
            <div
                class="w-[40px] h-[40px] bg-[#D9D9D9] rounded-full flex items-center justify-center overflow-hidden"
            >
                <img
                    v-if="authStore.user?.avatar"
                    :src="avatarUrl"
                    alt="avatar"
                    class="w-full h-full object-cover"
                />
                <i-solar-user-outline v-else class="text-2xl" />
            </div>
        </div>
    </header>
</template>
