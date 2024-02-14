import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";

export function getProducts() {
    return axios.get(`${BASE_URL}/products/`).then((response) => response.data);
}

export function getProductById(productId) {
    return axios
        .get(`${BASE_URL}/products/${productId}/`)
        .then((response) => response.data);
}

export function addProduct(product) {
    return axios
        .post(`${BASE_URL}/products/`, product)
        .then((response) => response.data);
}

export function updateProduct(productId, product) {
    return axios
        .put(`${BASE_URL}/products/${productId}/`, product)
        .then((response) => response.data);
}

export function deleteProduct(productId) {
    return axios
        .delete(`${BASE_URL}/products/${productId}/`)
        .then((response) => response.data);
}

export function getProductsByUniqueCode(uniqueCode) {
    return axios
        .get(`${BASE_URL}/products/?unique_code=${uniqueCode}`)
        .then((response) => response.data);
}
