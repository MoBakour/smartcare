<script setup lang="ts">
const props = defineProps<{
    modelValue: any;
}>();

const emit = defineEmits(["update:modelValue"]);

// Update patient data
const updatePatientData = (key: string, value: any) => {
    if (key.includes(".")) {
        const [parent, child] = key.split(".");
        emit("update:modelValue", {
            ...props.modelValue,
            [parent]: { ...props.modelValue[parent], [child]: value },
        });
    } else {
        emit("update:modelValue", { ...props.modelValue, [key]: value });
    }
};
</script>

<template>
    <div class="flex flex-col gap-4">
        <h2 class="text-gray-500 text-md font-semibold">Medical Information</h2>

        <div class="flex gap-10 max-xs:gap-5">
            <!-- col 1 -->
            <div class="flex flex-col gap-4 w-[140px] max-xs:w-[120px]">
                <!-- department -->
                <div class="flex flex-col gap-1">
                    <label for="department" class="text-gray-600 text-sm"
                        >Department</label
                    >
                    <select
                        id="department"
                        :value="modelValue.department"
                        @input="
                            updatePatientData(
                                'department',
                                ($event.target as HTMLSelectElement).value
                            )
                        "
                        class="rounded-md px-3 py-1.5 bg-white outline-none text-sm"
                    >
                        <option value="" disabled>Select</option>
                        <option>Cardiology</option>
                        <option>Neurology</option>
                        <option>ICU</option>
                        <option>ED</option>
                        <option>Pulmonology</option>
                        <option>Oncology</option>
                        <option>NICU</option>
                        <option>PACU</option>
                    </select>
                </div>

                <!-- wound type -->
                <div class="flex flex-col gap-1">
                    <label for="woundType" class="text-gray-600 text-sm"
                        >Wound Type</label
                    >
                    <select
                        id="woundType"
                        :value="modelValue.wound.type"
                        @input="
                            updatePatientData(
                                'wound.type',
                                ($event.target as HTMLSelectElement).value
                            )
                        "
                        class="rounded-md px-3 py-1.5 bg-white outline-none text-sm"
                    >
                        <option value="" disabled>Select</option>
                        <option>Burn</option>
                        <option>Puncture</option>
                        <option>Abrasion</option>
                        <option>Surgical Wound</option>
                        <option>Ulcer</option>
                        <option>Pressure Ulcer</option>
                        <option>Diabetic Ulcer</option>
                        <option>Laceration</option>
                    </select>
                </div>

                <!-- wound location -->
                <div class="flex flex-col gap-1">
                    <label for="woundLocation" class="text-gray-600 text-sm"
                        >Wound Location</label
                    >
                    <select
                        id="woundLocation"
                        :value="modelValue.wound.location"
                        @input="
                            updatePatientData(
                                'wound.location',
                                ($event.target as HTMLSelectElement).value
                            )
                        "
                        class="rounded-md px-3 py-1.5 bg-white outline-none text-sm"
                    >
                        <option value="" disabled>Select</option>
                        <option>Elbow</option>
                        <option>Hand</option>
                        <option>Head</option>
                        <option>Shoulder</option>
                        <option>Torso</option>
                        <option>Knee</option>
                        <option>Foot</option>
                        <option>Back</option>
                        <option>Arm</option>
                        <option>Leg</option>
                    </select>
                </div>

                <!-- wound severity -->
                <div class="flex flex-col gap-1">
                    <label for="woundSeverity" class="text-gray-600 text-sm"
                        >Wound Severity</label
                    >
                    <select
                        id="woundSeverity"
                        :value="modelValue.wound.severity"
                        @input="
                            updatePatientData(
                                'wound.severity',
                                ($event.target as HTMLSelectElement).value
                            )
                        "
                        class="rounded-md px-3 py-1.5 bg-white outline-none text-sm"
                    >
                        <option value="" disabled>Select</option>
                        <option>Moderate</option>
                        <option>Mild</option>
                        <option>Severe</option>
                    </select>
                </div>
            </div>

            <!-- col 2 -->
            <div class="flex flex-col gap-4 w-[140px] max-xs:w-[120px]">
                <!-- blood type -->
                <div class="flex flex-col gap-1">
                    <label for="bloodType" class="text-gray-600 text-sm"
                        >Blood Type</label
                    >
                    <select
                        id="bloodType"
                        :value="modelValue.bloodType"
                        @input="
                            updatePatientData(
                                'bloodType',
                                ($event.target as HTMLSelectElement).value
                            )
                        "
                        class="rounded-md px-3 py-1.5 bg-white outline-none text-sm"
                    >
                        <option value="" disabled>Select</option>
                        <option>O-</option>
                        <option>O+</option>
                        <option>A-</option>
                        <option>A+</option>
                        <option>B-</option>
                        <option>B+</option>
                        <option>AB-</option>
                        <option>AB+</option>
                    </select>
                </div>

                <!-- wound infected -->
                <div class="flex flex-col gap-1">
                    <label for="woundInfected" class="text-gray-600 text-sm"
                        >Wound Infected</label
                    >
                    <select
                        id="woundInfected"
                        :value="modelValue.wound.infected"
                        @input="
                            updatePatientData(
                                'wound.infected',
                                ($event.target as HTMLSelectElement).value
                            )
                        "
                        class="rounded-md px-3 py-1.5 bg-white outline-none text-sm"
                    >
                        <option value="" disabled>Select</option>
                        <option value="Yes">Yes</option>
                        <option value="No">No</option>
                    </select>
                </div>

                <!-- wound size -->
                <div class="flex flex-col gap-1">
                    <label for="woundSize" class="text-gray-600 text-sm"
                        >Wound Size</label
                    >
                    <div class="relative w-full">
                        <span
                            class="text-gray-400 pb-0.75 absolute top-1/2 left-2 -translate-y-1/2"
                            >cm</span
                        >
                        <input
                            id="woundSize"
                            :value="modelValue.wound.size"
                            @input="
                                updatePatientData(
                                    'wound.size',
                                    ($event.target as HTMLInputElement).value
                                )
                            "
                            type="number"
                            min="0"
                            placeholder="Size"
                            class="rounded-md py-1.5 pl-10 bg-white outline-none text-sm w-full"
                        />
                    </div>
                </div>

                <!-- wound treatment -->
                <div class="flex flex-col gap-1">
                    <label for="woundTreatment" class="text-gray-600 text-sm"
                        >Wound Treatment</label
                    >
                    <select
                        id="woundTreatment"
                        :value="modelValue.wound.treatment"
                        @input="
                            updatePatientData(
                                'wound.treatment',
                                ($event.target as HTMLSelectElement).value
                            )
                        "
                        class="rounded-md px-3 py-1.5 bg-white outline-none text-sm"
                    >
                        <option value="" disabled>Select</option>
                        <option>Surgical Debridement</option>
                        <option>Antibiotics (Oral)</option>
                        <option>Moist Wound Dressing</option>
                        <option>Negative Pressure Wound Therapy</option>
                        <option>Cleaning and Bandage</option>
                        <option>No Treatment (for mild cases)</option>
                        <option>Antibiotics (Topical)</option>
                    </select>
                </div>
            </div>
        </div>
    </div>
</template>
