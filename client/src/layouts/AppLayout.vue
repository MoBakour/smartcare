<script setup lang="ts">
import { computed, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useCommonStore } from "../stores/common.store";
import Header from "../components/layout/Header.vue";
import { useAuthStore } from "../stores/auth.store";

const route = useRoute();
const router = useRouter();
const commonStore = useCommonStore();
const authStore = useAuthStore();

const showLogoutPopup = ref(false);

const isCritical = computed(() => {
    return (
        commonStore.patientStatus === "Critical" &&
        /^\/patients\/[^/]+$/.test(route.path)
    );
});

const isActive = (path: string, nested: boolean = false) => {
    if (nested) {
        return route.path.startsWith(path);
    } else {
        return route.path === path;
    }
};

const handleLogout = () => {
    authStore.logout();
    commonStore.setSidebarOpen(false);
    router.push("/auth");
};

const greeting = new Date().getHours() < 12 ? "Good Morning" : "Good Evening";

const username = computed(() => {
    return authStore.user?.username.split(" ")[0];
});

const sidebarOpen = computed(() => {
    return commonStore.sidebarOpen;
});
</script>

<template>
    <div
        class="layout flex"
        :class="{
            'bg-gradient-to-t from-crimson/25 to-transparent bg-fixed':
                isCritical,
        }"
    >
        <!-- responsive sidebar dark overlay -->
        <div
            class="fixed inset-0 bg-black/70 z-10 transition-all backdrop-blur-xs"
            :class="{ 'opacity-0 pointer-events-none': !sidebarOpen }"
            @click="commonStore.setSidebarOpen(false)"
        ></div>

        <!-- sidebar -->
        <div
            class="sidebar sticky top-0 left-0 h-screen flex flex-col gap-8 bg-[#D9D9D9] w-[300px] max-lg:absolute rounded-tr-[50px] overflow-hidden z-10 transition-all"
            :class="{
                'max-lg:translate-x-0': sidebarOpen,
                'max-lg:-translate-x-full': !sidebarOpen,
            }"
        >
            <!-- top -->
            <div>
                <div class="bg-theme h-[100px] relative z-10">
                    <img src="../assets/images/logo.png" class="w-[200px]" />
                </div>
                <svg
                    width="342"
                    height="61"
                    viewBox="0 0 342 61"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <path
                        fill-rule="evenodd"
                        clip-rule="evenodd"
                        d="M0 24.1897L19.095 34.2687C37.905 44.3478 76.095 64.5058 114 60.4742C151.905 56.4426 190.095 28.2213 228 24.1897C265.905 20.1581 304.095 40.3161 322.905 50.3952L342 60.4742V-3.8147e-06H322.905C304.095 -3.8147e-06 265.905 -3.8147e-06 228 -3.8147e-06C190.095 -3.8147e-06 151.905 -3.8147e-06 114 -3.8147e-06C76.095 -3.8147e-06 37.905 -3.8147e-06 19.095 -3.8147e-06H0V24.1897Z"
                        fill="#50E3C2"
                    />
                </svg>
            </div>

            <!-- good morning -->
            <div class="flex flex-col ml-5">
                <p>
                    <span class="text-lg">{{ greeting }}</span
                    ><span class="text-lg"> Dr.</span>
                    <br />
                    <span class="text-2xl font-bold">{{ username }}</span>
                </p>
            </div>

            <!-- nav -->
            <nav>
                <ul class="flex flex-col gap-4">
                    <li class="w-fit">
                        <router-link
                            to="/patients"
                            class="flex items-center hover:opacity-100 transition"
                            :class="
                                isActive('/patients', true)
                                    ? 'opacity-100'
                                    : 'opacity-60'
                            "
                            @click="commonStore.setSidebarOpen(false)"
                        >
                            <div
                                class="transition-all h-[5px] rounded-r-[100px] bg-black"
                                :class="
                                    isActive('/patients', true)
                                        ? 'w-[40px]'
                                        : 'w-0'
                                "
                            />
                            <i-healthicons-inpatient-outline-24px
                                class="text-3xl transition-all"
                                :class="
                                    isActive('/patients', true)
                                        ? 'ml-4'
                                        : 'ml-8'
                                "
                            />
                            <span class="text-2xl ml-2">Patients</span>
                        </router-link>
                    </li>
                    <li class="w-fit">
                        <router-link
                            to="/settings"
                            class="flex items-center hover:opacity-100 transition"
                            :class="
                                isActive('/settings')
                                    ? 'opacity-100'
                                    : 'opacity-60'
                            "
                            @click="commonStore.setSidebarOpen(false)"
                        >
                            <div
                                class="transition-all h-[5px] rounded-r-[100px] bg-black"
                                :class="
                                    isActive('/settings') ? 'w-[40px]' : 'w-0'
                                "
                            />
                            <i-mdi-settings
                                class="text-3xl transition-all"
                                :class="isActive('/settings') ? 'ml-4' : 'ml-8'"
                            />
                            <span class="text-2xl ml-2">Settings</span>
                        </router-link>
                    </li>
                    <li class="w-fit">
                        <router-link
                            to="/about"
                            class="flex items-center hover:opacity-100 transition"
                            :class="
                                isActive('/about')
                                    ? 'opacity-100'
                                    : 'opacity-60'
                            "
                            @click="commonStore.setSidebarOpen(false)"
                        >
                            <div
                                class="transition-all h-[5px] rounded-r-[100px] bg-black"
                                :class="isActive('/about') ? 'w-[40px]' : 'w-0'"
                            />
                            <i-akar-icons-info
                                class="text-3xl transition-all"
                                :class="isActive('/about') ? 'ml-4' : 'ml-8'"
                            />
                            <span class="text-2xl ml-2">About</span>
                        </router-link>
                    </li>
                    <li class="w-fit">
                        <button
                            class="flex items-center text-crimson opacity-60 hover:opacity-100 transition cursor-pointer"
                            @click="showLogoutPopup = true"
                        >
                            <i-mdi-logout class="text-3xl ml-8" />
                            <span class="text-2xl ml-2">Logout</span>
                        </button>
                    </li>
                </ul>
            </nav>
        </div>

        <!-- logout popup -->
        <div
            class="fixed inset-0 flex items-center justify-center bg-black/70 z-10 transition-all"
            :class="{ 'opacity-0 pointer-events-none': !showLogoutPopup }"
        >
            <div class="bg-white p-5 rounded-lg w-[300px]">
                <p class="text-center">Are you sure you want to logout?</p>
                <div class="flex flex-col gap-2 mt-5">
                    <button
                        class="bg-crimson text-white font-bold w-full h-[30px] text-sm rounded-md flex items-center justify-center cursor-pointer hover:opacity-80 transition"
                        @click="handleLogout"
                        title="Logout"
                    >
                        Logout <i-mdi-logout class="text-sm ml-2" />
                    </button>
                    <button
                        class="bg-gray-300 text-gray-700 w-full h-[30px] text-sm rounded-md cursor-pointer hover:opacity-80 transition"
                        @click="showLogoutPopup = false"
                        title="Cancel"
                    >
                        Cancel
                    </button>
                </div>
            </div>
        </div>

        <!-- page content -->
        <div class="px-12 max-md:px-6 max-xs:px-4 flex-1">
            <Header />
            <div class="max-w-[900px] mx-auto">
                <RouterView />
            </div>
        </div>
    </div>
</template>

<style scoped>
/* animate slide-in */
@keyframes slide-in {
    from {
        transform: translateX(-100%);
    }
    to {
        transform: translateX(0);
    }
}

/* animate fade-in */
@keyframes fade-in {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

.sidebar {
    animation: slide-in 0.5s ease-in-out;
}

.layout {
    animation: fade-in 0.5s ease-in-out;
}
</style>
