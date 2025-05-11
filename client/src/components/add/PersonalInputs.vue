<script setup lang="ts">
const props = defineProps<{
    modelValue: any;
}>();

const emit = defineEmits(["update:modelValue"]);

const handleFileChange = (event: Event) => {
    const target = event.target as HTMLInputElement;
    const file = target.files?.[0];

    if (file) {
        emit("update:modelValue", {
            ...props.modelValue,
            avatarFile: file,
        });

        const reader = new FileReader();
        reader.onload = () => {
            emit("update:modelValue", {
                ...props.modelValue,
                avatarPreview: reader.result as string,
            });
        };
        reader.readAsDataURL(file);
    }
};

// Update patient data
const updatePatientData = (key: string, value: any) => {
    emit("update:modelValue", { ...props.modelValue, [key]: value });
};
</script>

<template>
    <div class="flex flex-col gap-4">
        <h2 class="text-gray-500 text-md font-semibold">
            Personal Information
        </h2>

        <!-- avatar -->
        <label
            class="w-[80px] h-[80px] bg-[#D9D9D9] m-auto rounded-full flex items-center justify-center overflow-hidden cursor-pointer hover:opacity-80 transition"
            title="Upload Profile Picture"
            for="avatar"
        >
            <template v-if="modelValue.avatarPreview">
                <img
                    :src="modelValue.avatarPreview"
                    alt="Profile Preview"
                    class="w-full h-full object-cover"
                />
            </template>
            <template v-else>
                <i-solar-user-outline class="text-4xl" />
            </template>
        </label>

        <!-- hidden file input -->
        <input
            type="file"
            id="avatar"
            accept="image/*"
            class="hidden"
            @change="handleFileChange"
        />

        <!-- name -->
        <div class="flex flex-col gap-1">
            <label for="name" class="text-gray-600 text-sm">Patient Name</label>
            <input
                id="name"
                :value="modelValue.name"
                @input="
                    updatePatientData(
                        'name',
                        ($event.target as HTMLInputElement).value
                    )
                "
                type="text"
                placeholder="Enter name"
                class="rounded-md px-3 py-1.5 bg-white outline-none text-sm"
            />
        </div>

        <!-- gender -->
        <div class="flex justify-between">
            <button
                type="button"
                class="w-[80px] py-1.5 rounded-md text-white font-semibold text-sm transition hover:opacity-80 cursor-pointer"
                :class="
                    modelValue.gender === 'Male'
                        ? 'bg-blue-400'
                        : 'bg-gray-300 text-black'
                "
                @click="updatePatientData('gender', 'Male')"
            >
                Male
            </button>
            <button
                type="button"
                class="w-[80px] py-1.5 rounded-md text-white font-semibold text-sm transition hover:opacity-80 cursor-pointer"
                :class="
                    modelValue.gender === 'Female'
                        ? 'bg-pink-300'
                        : 'bg-gray-300 text-black'
                "
                @click="updatePatientData('gender', 'Female')"
            >
                Female
            </button>
        </div>

        <!-- age + bed -->
        <div class="flex justify-between">
            <div class="flex flex-col gap-1">
                <label for="age" class="text-gray-600 text-sm">Age</label>
                <input
                    id="age"
                    :value="modelValue.age"
                    @input="
                        updatePatientData(
                            'age',
                            ($event.target as HTMLInputElement).value
                        )
                    "
                    type="number"
                    placeholder="Age"
                    class="rounded-md py-1.5 pl-3 bg-white outline-none w-[80px] text-sm"
                />
            </div>
            <div class="flex flex-col gap-1">
                <label for="bed" class="text-gray-600 text-sm">Bed</label>
                <div class="relative">
                    <span
                        class="text-gray-400 absolute top-1/2 left-2 -translate-y-1/2"
                        >#</span
                    >
                    <input
                        id="bed"
                        :value="modelValue.bed"
                        @input="
                            updatePatientData(
                                'bed',
                                ($event.target as HTMLInputElement).value
                            )
                        "
                        type="number"
                        placeholder="Bed"
                        class="rounded-md py-1.5 pl-6 bg-white outline-none w-[80px] text-sm"
                    />
                </div>
            </div>
        </div>
    </div>
</template>
