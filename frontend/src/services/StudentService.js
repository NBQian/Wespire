import axios from "axios";

const BASE_URL = "http://18.224.107.62:8000/";

export function getStudents() {
    return axios.get(`${BASE_URL}/clients/`).then((response) => response.data);
}

export function getStudentById(summaryId) {
    return axios
        .get(`${BASE_URL}/clients/${summaryId}/`)
        .then((response) => response.data);
}

export function addStudent(summary) {
    return axios
        .post(`${BASE_URL}/clients/`, summary)
        .then((response) => response.data);
}

export function updateStudent(summaryId, summary) {
    return axios
        .put(`${BASE_URL}/clients/${summaryId}/`, summary)
        .then((response) => response.data);
}

export function deleteStudent(summaryId) {
    return axios
        .delete(`${BASE_URL}/clients/${summaryId}/`)
        .then((response) => response.data);
}
