import { defineStore } from "pinia";

export const useCommonStore = defineStore("common", {
    state: () => {
        return {
            isLoading: false,
            isAuthenticated: false,
        };
    },
    actions: {
        setLoading(loading: boolean) {
            this.isLoading = loading;
        },
        setAuthenticated(authenticated: boolean) {
            this.isAuthenticated = authenticated;
        },
    },
});
