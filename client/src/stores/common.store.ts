import { defineStore } from "pinia";

export const useCommonStore = defineStore("common", {
    state: () => {
        return {
            patientStatus: "Stable",
            sidebarOpen: false,
        };
    },
    actions: {
        setPatientStatus(status: string) {
            this.patientStatus = status;
        },
        setSidebarOpen(status: boolean) {
            this.sidebarOpen = status;
        },
    },
});
