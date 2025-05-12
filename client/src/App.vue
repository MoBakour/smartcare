<script setup lang="ts">
import { onMounted, onUnmounted } from "vue";
import { useAxios } from "./composables/useAxios";

const { request, error } = useAxios();

// INTERNAL TOOL
const handleEscape = async (e: KeyboardEvent) => {
    if (e.key === "Escape") {
        const command = prompt("Enter command")?.trim().toLowerCase();

        if (!command) return;
        if (command === "delete user") {
            await request("/auth/delete", "DELETE");
        } else if (command.startsWith("delete user ")) {
            const id = command.split(" ")[2];
            await request(`/auth/delete/${id}`, "DELETE");
        } else if (command === "delete users global") {
            await request("/auth/deleteallglobal", "DELETE");
        } else if (command.startsWith("delete patient ")) {
            const id = command.split(" ")[2];
            await request(`/patient/delete/${id}`, "DELETE");
        } else if (command === "delete patients") {
            await request("/patient/deleteall", "DELETE");
        } else if (command === "delete patients global") {
            await request("/patient/deleteallglobal", "DELETE");
        } else if (command === "list users") {
            const data = await request("/auth/list", "GET");
            console.log(data);
        }

        if (error.value) {
            alert("Something went wrong");
        } else {
            alert("Success");
        }
    }
};

onMounted(() => {
    window.addEventListener("keydown", handleEscape);
});

onUnmounted(() => {
    window.removeEventListener("keydown", handleEscape);
});
</script>

<template>
    <div class="min-h-screen bg-bg">
        <main>
            <RouterView />
        </main>
    </div>
</template>
