import axios from "axios";
import store from "./store";
import { refreshAccessToken, logout } from "./actions/auth";

axios.defaults.baseURL = process.env.REACT_APP_API_URL;

axios.interceptors.request.use(
    (config) => {
        const state = store.getState();
        const token = state.auth.access;
        if (token) {
            config.headers["Authorization"] = `JWT ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

axios.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            try {
                if (!originalRequest.url.includes("/auth/jwt/refresh/")) {
                    await store.dispatch(refreshAccessToken());
                    const state = store.getState();
                    const newToken = state.auth.access;
                    originalRequest.headers[
                        "Authorization"
                    ] = `JWT ${newToken}`;
                    return axios(originalRequest);
                }
            } catch (refreshError) {
                return Promise.reject(refreshError);
            }
        }
        return Promise.reject(error);
    }
);
