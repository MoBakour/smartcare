import { createRouter, createWebHistory } from "vue-router";
import AuthView from "../views/AuthView.vue";
import PatientsView from "../views/PatientsView.vue";
import SettingsView from "../views/SettingsView.vue";
import PatientView from "../views/PatientView.vue";
import AddPatientView from "../views/AddPatientView.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            redirect: "/patients",
        },
        {
            path: "/auth",
            name: "auth",
            component: AuthView,
        },
        {
            path: "/patients",
            name: "patients",
            component: PatientsView,
        },
        {
            path: "/settings",
            name: "settings",
            component: SettingsView,
        },
        {
            path: "/patient/:id",
            name: "patient",
            component: PatientView,
        },
        {
            path: "/new",
            name: "new",
            component: AddPatientView,
        },
    ],
});

export default router;
