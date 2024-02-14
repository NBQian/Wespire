import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";

export function getFuturePlans() {
    return axios
        .get(`${BASE_URL}/future-plans/`)
        .then((response) => response.data);
}

export function getFuturePlanById(futurePlanId) {
    return axios
        .get(`${BASE_URL}/future-plans/${futurePlanId}/`)
        .then((response) => response.data);
}

export function addFuturePlan(futurePlan) {
    return axios
        .post(`${BASE_URL}/future-plans/`, futurePlan)
        .then((response) => response.data);
}

export function updateFuturePlan(futurePlanId, futurePlan) {
    return axios
        .put(`${BASE_URL}/future-plans/${futurePlanId}/`, futurePlan)
        .then((response) => response.data);
}

export function deleteFuturePlan(futurePlanId) {
    return axios
        .delete(`${BASE_URL}/future-plans/${futurePlanId}/`)
        .then((response) => response.data);
}

export function getFuturePlansByUniqueCode(uniqueCode) {
    return axios
        .get(`${BASE_URL}/future-plans/?unique_code=${uniqueCode}`)
        .then((response) => response.data);
}
