<script setup lang="ts">
import { useRoute } from "vue-router";
import Header from "../components/Header.vue";

const route = useRoute();

const isActive = (path: string, nested: boolean = false) => {
    if (nested) {
        return route.path.startsWith(path);
    } else {
        return route.path === path;
    }
};
</script>

<template>
    <div class="flex">
        <!-- side bar -->
        <div
            class="sidebar sticky top-0 left-0 h-screen flex flex-col gap-8 bg-[#D9D9D9] w-[300px] rounded-tr-[50px] overflow-hidden"
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
                    <span class="text-lg">Good Morning Dr.</span>
                    <br />
                    <span class="text-2xl font-bold">Mohamed</span>
                </p>
            </div>

            <!-- nav -->
            <nav>
                <ul class="flex flex-col gap-4">
                    <li class="w-fit">
                        <router-link
                            to="/patients"
                            class="flex items-center gap-2 hover:opacity-100 transition"
                            :class="
                                isActive('/patients', true)
                                    ? 'opacity-100'
                                    : 'opacity-60'
                            "
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
                                        ? 'ml-2'
                                        : 'ml-6'
                                "
                            />
                            <span class="text-2xl">Patients</span>
                        </router-link>
                    </li>
                    <li class="w-fit">
                        <router-link
                            to="/settings"
                            class="flex items-center gap-2 hover:opacity-100 transition"
                            :class="
                                isActive('/settings')
                                    ? 'opacity-100'
                                    : 'opacity-60'
                            "
                        >
                            <div
                                class="transition-all h-[5px] rounded-r-[100px] bg-black"
                                :class="
                                    isActive('/settings') ? 'w-[40px]' : 'w-0'
                                "
                            />
                            <i-mdi-settings
                                class="text-3xl transition-all"
                                :class="isActive('/settings') ? 'ml-2' : 'ml-6'"
                            />
                            <span class="text-2xl">Settings</span>
                        </router-link>
                    </li>
                    <li class="w-fit">
                        <button
                            class="flex items-center gap-2 text-crimson opacity-60 hover:opacity-100 transition cursor-pointer"
                        >
                            <i-mdi-logout class="text-3xl ml-6" />
                            <span class="text-2xl">Logout</span>
                        </button>
                    </li>
                </ul>
            </nav>
        </div>

        <!-- page content -->
        <div class="px-12 flex-1">
            <Header />
            <RouterView />
        </div>
    </div>
</template>

<style scoped>
/* animate sidebar in */
@keyframes slide-in {
    from {
        transform: translateX(-100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

.sidebar {
    animation: slide-in 0.5s ease-in-out;
}
</style>
