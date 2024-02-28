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
    TOKEN_EXPIRED,
    RESEND_ACTIVATION_EMAIL_SUCCESS,
    RESEND_ACTIVATION_EMAIL_FAIL,
    CLEAR_ERRORS,
} from "../actions/types";

const initialState = {
    access: localStorage.getItem("access"),
    refresh: localStorage.getItem("refresh"),
    isAuthenticated: null,
    user: null,
    error: null,
};

function authReducer(state = initialState, action) {
    const { type, payload } = action;

    switch (type) {
        case AUTHENTICATED_SUCCESS:
            return {
                ...state,
                isAuthenticated: true,
            };
        case LOGIN_SUCCESS:
            localStorage.setItem("access", payload.access);
            localStorage.setItem("refresh", payload.refresh);
            return {
                ...state,
                isAuthenticated: true,
                access: payload.access,
                refresh: payload.refresh,
                error: null,
            };
        case USER_LOADED_SUCCESS:
            return {
                ...state,
                user: payload,
            };
        case AUTHENTICATED_FAIL:
            return {
                ...state,
                isAuthenticated: false,
            };
        case USER_LOADED_FAIL:
            return {
                ...state,
                user: null,
            };
        case LOGIN_FAIL:
            localStorage.removeItem("access");
            localStorage.removeItem("refresh");
            return {
                ...state,
                access: null,
                refresh: null,
                isAuthenticated: false,
                user: null,
                error: payload.error,
            };
        case SIGNUP_SUCCESS:
            return {
                ...state,
                isAuthenticated: false,
                signUpSuccessEmail: payload.email, // Store the user's email upon successful signup
                error: null, // Reset any previous errors
            };
        case SIGNUP_FAIL:
        case LOGOUT:
            localStorage.removeItem("access");
            localStorage.removeItem("refresh");
            return {
                ...state,
                access: null,
                refresh: null,
                isAuthenticated: false,
                user: null,
                error: null,
            };
        case PASSWORD_RESET_SUCCESS:
        case PASSWORD_RESET_FAIL:
        case PASSWORD_RESET_CONFIRM_SUCCESS:
        case PASSWORD_RESET_CONFIRM_FAIL:
        case ACTIVATION_SUCCESS:
        case ACTIVATION_FAIL:
            return {
                ...state,
            };
        case TOKEN_EXPIRED:
            localStorage.removeItem("access");
            localStorage.removeItem("refresh");
            return {
                ...state,
                access: null,
                refresh: null,
                isAuthenticated: false,
                user: null,
                error: "Session expired. Please login again.",
            };

        case RESEND_ACTIVATION_EMAIL_SUCCESS:
            return {
                ...state,
                resendActivationEmailSuccess: true,
                resendActivationEmailError: null,
            };
        case RESEND_ACTIVATION_EMAIL_FAIL:
            return {
                ...state,
                resendActivationEmailSuccess: false,
                resendActivationEmailError: payload.error,
            };
        case CLEAR_ERRORS:
            return {
                ...state,
                error: null,
            };
        default:
            return state;
    }
}

export default authReducer;
