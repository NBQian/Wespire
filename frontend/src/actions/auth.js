import axios from "axios";
import {
    LOGIN_SUCCESS,
    LOGIN_FAIL,
    USER_LOADED_SUCCESS,
    USER_LOADED_FAIL,
    AUTHENTICATED_SUCCESS,
    AUTHENTICATED_FAIL,
    PASSWORD_RESET_SUCCESS,
    PASSWORD_RESET_FAIL,
    PASSWORD_RESET_CONFIRM_SUCCESS,
    PASSWORD_RESET_CONFIRM_FAIL,
    SIGNUP_SUCCESS,
    SIGNUP_FAIL,
    ACTIVATION_SUCCESS,
    ACTIVATION_FAIL,
    LOGOUT,
    RESEND_ACTIVATION_EMAIL_SUCCESS,
    RESEND_ACTIVATION_EMAIL_FAIL,
    CLEAR_ERRORS,
} from "./types";

export const load_user = () => async (dispatch) => {
    if (localStorage.getItem("access")) {
        const config = {
            headers: {
                "Content-Type": "application/json",
                Authorization: `JWT ${localStorage.getItem("access")}`,
                Accept: "application/json",
            },
        };

        try {
            const res = await axios.get(
                `${process.env.REACT_APP_API_URL}/auth/users/me/`,
                config
            );

            dispatch({
                type: USER_LOADED_SUCCESS,
                payload: res.data,
            });
        } catch (err) {
            dispatch({
                type: USER_LOADED_FAIL,
            });
        }
    } else {
        dispatch({
            type: USER_LOADED_FAIL,
        });
    }
};

export const refreshAccessToken = () => async (dispatch) => {
    const refresh = localStorage.getItem("refresh");
    if (refresh) {
        const body = JSON.stringify({ refresh });
        try {
            const response = await axios.post(
                `${process.env.REACT_APP_API_URL}/auth/jwt/refresh/`,
                body,
                {
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );
            dispatch({
                type: LOGIN_SUCCESS,
                payload: response.data,
            });
        } catch (error) {
            console.log("Error refreshing access token:", error);
            dispatch({ type: AUTHENTICATED_FAIL });
        }
    }
};

export const checkAuthenticated = () => async (dispatch) => {
    if (localStorage.getItem("access")) {
        const config = {
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
        };

        const body = JSON.stringify({ token: localStorage.getItem("access") });

        try {
            const res = await axios.post(
                `${process.env.REACT_APP_API_URL}/auth/jwt/verify/`,
                body,
                config
            );

            if (res.data.code !== "token_not_valid") {
                dispatch({
                    type: AUTHENTICATED_SUCCESS,
                });
            } else {
                dispatch({
                    type: AUTHENTICATED_FAIL,
                });
            }
        } catch (err) {
            dispatch({
                type: AUTHENTICATED_FAIL,
            });
        }
    } else {
        dispatch({
            type: AUTHENTICATED_FAIL,
        });
    }
};

export const login = (email, password) => async (dispatch) => {
    const config = {
        headers: {
            "Content-Type": "application/json",
        },
    };

    const body = JSON.stringify({ email, password });

    try {
        const res = await axios.post(
            `${process.env.REACT_APP_API_URL}/auth/jwt/create/`,
            body,
            config
        );
        dispatch({
            type: LOGIN_SUCCESS,
            payload: res.data,
        });

        dispatch(load_user());
    } catch (err) {
        dispatch({
            type: LOGIN_FAIL,
            payload: {
                error:
                    // err.response.data.detail ||
                    "Login failed. Please check your email and password and try again.",
            },
        });
    }
};

export const signup =
    (name, email, password, re_password) => async (dispatch) => {
        const config = {
            headers: {
                "Content-Type": "application/json",
            },
        };

        const body = JSON.stringify({
            name,
            email,
            password,
            re_password,
        });

        try {
            const res = await axios.post(
                `${process.env.REACT_APP_API_URL}/auth/users/`,
                body,
                config
            );

            dispatch({
                type: SIGNUP_SUCCESS,
                payload: { message: "Verification email sent", email: email },
            });
        } catch (err) {
            dispatch({
                type: SIGNUP_FAIL,
            });
        }
    };

export const verify = (uid, token) => async (dispatch) => {
    const config = {
        headers: {
            "Content-Type": "application/json",
        },
    };

    const body = JSON.stringify({ uid, token });

    try {
        await axios.post(
            `${process.env.REACT_APP_API_URL}/auth/users/activation/`,
            body,
            config
        );

        dispatch({
            type: ACTIVATION_SUCCESS,
        });
    } catch (err) {
        dispatch({
            type: ACTIVATION_FAIL,
        });
    }
};

export const reset_password = (email) => async (dispatch) => {
    const config = {
        headers: {
            "Content-Type": "application/json",
        },
    };

    const body = JSON.stringify({ email });

    try {
        await axios.post(
            `${process.env.REACT_APP_API_URL}/auth/users/reset_password/`,
            body,
            config
        );

        dispatch({
            type: PASSWORD_RESET_SUCCESS,
        });
    } catch (err) {
        dispatch({
            type: PASSWORD_RESET_FAIL,
        });
    }
};

export const reset_password_confirm =
    (uid, token, new_password, re_new_password) => async (dispatch) => {
        const config = {
            headers: {
                "Content-Type": "application/json",
            },
        };

        const body = JSON.stringify({
            uid,
            token,
            new_password,
            re_new_password,
        });

        try {
            await axios.post(
                `${process.env.REACT_APP_API_URL}/auth/users/reset_password_confirm/`,
                body,
                config
            );

            dispatch({
                type: PASSWORD_RESET_CONFIRM_SUCCESS,
            });
        } catch (err) {
            dispatch({
                type: PASSWORD_RESET_CONFIRM_FAIL,
            });
        }
    };

export const logout = () => (dispatch) => {
    dispatch({
        type: LOGOUT,
    });
};

export const resendActivationEmail = (email) => async (dispatch) => {
    try {
        const config = {
            headers: {
                "Content-Type": "application/json",
            },
        };
        const body = JSON.stringify({ email });
        await axios.post(
            `${process.env.REACT_APP_API_URL}/auth/users/resend_activation/`,
            body,
            config
        );
        dispatch({
            type: RESEND_ACTIVATION_EMAIL_SUCCESS,
        });
    } catch (err) {
        dispatch({
            type: RESEND_ACTIVATION_EMAIL_FAIL,
        });
    }
};

export const clearErrors = () => {
    return {
        type: CLEAR_ERRORS,
    };
};
