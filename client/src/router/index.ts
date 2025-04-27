import { createRouter, createWebHistory } from "vue-router";
import AuthView from "../views/AuthView.vue";
import PatientsView from "../views/PatientsView.vue";
import SettingsView from "../views/SettingsView.vue";
import PatientView from "../views/PatientView.vue";
import AddPatientView from "../views/AddPatientView.vue";
import NotFound from "../views/NotFound.vue";
import AboutView from "../views/AboutView.vue";
import AppLayout from "../layouts/AppLayout.vue";

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
            path: "/",
            component: AppLayout,
            children: [
                {
                    path: "patients",
                    name: "patients",
                    component: PatientsView,
                },
                {
                    path: "settings",
                    name: "settings",
                    component: SettingsView,
                },
                {
                    path: "patients/:id",
                    name: "patient",
                    component: PatientView,
                },
                {
                    path: "new",
                    name: "new",
                    component: AddPatientView,
                },
                {
                    path: "about",
                    name: "about",
                    component: AboutView,
                },
            ],
        },
        {
            path: "/:pathMatch(.*)*",
            name: "not-found",
            component: NotFound,
        },
    ],
});

export default router;
