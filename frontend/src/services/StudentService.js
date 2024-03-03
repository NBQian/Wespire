import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_URL;

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
        .then((response) => response.data)
        .catch((error) => {
            console.log(error.response.status);
        });
}

export function deleteStudent(summaryId) {
    return axios
        .delete(`${BASE_URL}/clients/${summaryId}/`)
        .then((response) => response.data);
}
