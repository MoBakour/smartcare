<script lang="ts" setup>
import { ref } from "vue";

const emit = defineEmits(["connect"]);

const isDragging = ref(false);

const handleUpload = (event: Event) => {
    let file: File | undefined;

    if (event.target instanceof HTMLInputElement) {
        file = (event.target as HTMLInputElement).files?.[0];
    } else if (event.target instanceof HTMLLabelElement) {
        file = (event as DragEvent).dataTransfer?.files[0];
    }

    if (file) {
        emit("connect", file);
    }
};
</script>

<template>
    <!-- drag drop upload box -->
    <div class="">
        <div>
            <p class="my-5 text-lg font-bold">
                Connect patient to smart wound dressing
            </p>
            <label
                class="w-full h-[120px] flex flex-col gap-2 justify-center items-center opacity-70 text-sm border-dashed border-2 border-gray-400 text-gray-400 font-bold rounded-lg transition hover:opacity-100 cursor-pointer"
                for="file"
                :class="{ 'bg-gray-300': isDragging }"
                @dragover.prevent="isDragging = true"
                @dragleave.prevent="isDragging = false"
                @drop.prevent="handleUpload"
            >
                <i-mdi-upload class="text-2xl" />
                <span>Drag and drop patient data source here</span>
            </label>
            <input
                type="file"
                accept=".csv"
                id="file"
                class="hidden"
                @change="handleUpload"
            />
        </div>
    </div>
</template>
