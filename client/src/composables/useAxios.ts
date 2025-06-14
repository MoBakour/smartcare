import api from "../api/axios";
import { ref } from "vue";

export const useAxios = () => {
    const isLoading = ref(false);
    const error = ref<string | null>(null);

    const request = async (
        url: string,
        method: string,
        data?: any,
        options?: any
    ) => {
        isLoading.value = true;
        error.value = null;

        try {
            const response = await api.request({
                url,
                method,
                data,
                ...options,
            });

            return response.data;
        } catch (err: any) {
            console.error(err);
            error.value =
                err.response?.data?.error ||
                err.message ||
                err.error ||
                "An error occurred";
        } finally {
            isLoading.value = false;
        }
    };

    return { isLoading, error, request };
};
