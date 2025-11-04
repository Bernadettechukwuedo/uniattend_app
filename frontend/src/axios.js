import axios from 'axios';
import { useAuthStore } from './stores/auth';
const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
});
api.interceptors.request.use(
    config => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    error => Promise.reject(error)
);

api.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config;


        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const authStore = useAuthStore();
                const refreshToken = localStorage.getItem('refresh_token');

                console.log("Refreshing token with:", { refresh_token: refreshToken });
                console.log('Attempting to refresh token with:', refreshToken);

                const res = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/auth/refresh-token`, {
                    refresh_token: refreshToken
                });

                const newAccessToken = res.data.access_token;

                // Save new token
                authStore.token = newAccessToken;
                localStorage.setItem('token', newAccessToken);

                // Retry original request
                originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
                return api(originalRequest);
            } catch (refreshError) {
                const authStore = useAuthStore();
                authStore.logout();
                window.location.href = '/';
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

export default api;
