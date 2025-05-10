import { defineStore } from "pinia";

export const useCommonStore = defineStore("common", {
    state: () => {
        return {
            patientStatus: "Stable",
        };
    },
    actions: {
        setPatientStatus(status: string) {
            this.patientStatus = status;
        },
    },
});
