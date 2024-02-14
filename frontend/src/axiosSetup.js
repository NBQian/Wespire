// src/axiosSetup.js
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
                // Attempt to refresh token only if the failing request is not a refresh token request
                if (!originalRequest.url.includes("/auth/jwt/refresh/")) {
                    await store.dispatch(refreshAccessToken()); // Attempt to refresh token
                    const state = store.getState();
                    const newToken = state.auth.access;
                    originalRequest.headers[
                        "Authorization"
                    ] = `JWT ${newToken}`;
                    return axios(originalRequest); // Retry the original request with new token
                }
            } catch (refreshError) {
                // Handle failure: e.g., logout user or redirect to login
                return Promise.reject(refreshError);
            }
        }
        // If refresh token request itself fails, do not retry
        return Promise.reject(error);
    }
);
