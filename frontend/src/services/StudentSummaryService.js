import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_URL;

export function getStudentSummaries() {
    return axios
        .get(`${BASE_URL}/client-summaries/`)
        .then((response) => response.data);
}

export function getStudentSummaryById(summaryId) {
    return axios
        .get(`${BASE_URL}/client-summaries/${summaryId}/`)
        .then((response) => response.data);
}

export function addStudentSummary(summary) {
    return axios
        .post(`${BASE_URL}/client-summaries/`, summary)
        .then((response) => response.data);
}

export function updateStudentSummary(summaryId, summary) {
    return axios
        .put(`${BASE_URL}/client-summaries/${summaryId}/`, summary)
        .then((response) => response.data);
}

export function deleteStudentSummary(summaryId) {
    return axios
        .delete(`${BASE_URL}/client-summaries/${summaryId}/`)
        .then((response) => response.data);
}
