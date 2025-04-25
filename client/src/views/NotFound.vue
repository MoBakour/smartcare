<template>
    <div class="min-h-screen flex items-center justify-center relative">
        <!-- squares -->
        <div class="fixed inset-0">
            <div
                class="w-[600px] h-[600px] bg-theme rounded-[100px] rotate-[30deg] opacity-40 fixed top-0 -translate-x-1/4 -translate-y-1/4 pointer-events-none blur-xl"
            />
            <div
                class="w-[450px] h-[450px] bg-theme rounded-[80px] rotate-[60deg] opacity-40 fixed bottom-0 right-0 translate-x-1/4 translate-y-1/4 pointer-events-none blur-xl"
            />
        </div>

        <!-- not found content -->
        <div
            class="w-[300px] h-[300px] bg-theme rounded-[40px] -rotate-20 relative"
        >
            <div
                class="text-center text-white rotate-20 absolute inset-0 flex flex-col items-center justify-center"
            >
                <h1 class="text-8xl font-bold">404</h1>
                <p class="text-2xl mb-8">Page not found</p>
                <router-link
                    to="/"
                    class="font-bold text-lg flex flex-col items-center"
                >
                    <span>Go to Home</span>
                    <i-mynaui-arrow-long-left class="text-xl font-bold" />
                </router-link>
            </div>
        </div>
    </div>
</template>
