import { defineStore } from "pinia";

interface IAuth {
    token: string | null;
    user: IUser | null;
}

export const useAuthStore = defineStore("auth", {
    state: (): IAuth => {
        return {
            token: localStorage.getItem("token"),
            user: JSON.parse(localStorage.getItem("user") || "null"),
        };
    },

    getters: {
        isAuthenticated: (state) => state.token !== null,
    },

    actions: {
        login(token: string, user: IUser | null) {
            this.token = token;
            this.user = user;
            localStorage.setItem("token", token);
            localStorage.setItem("user", JSON.stringify(user));
        },
        logout() {
            this.token = null;
            this.user = null;
            localStorage.removeItem("token");
            localStorage.removeItem("user");
        },
    },
});
