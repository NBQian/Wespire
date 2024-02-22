import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { BrowserRouter } from "react-router-dom";
import Layout from "./hocs/Layout";
import ProtectedRoutes from "./components/ProtectedRoutes";
import { Provider } from "react-redux";
import store from "./store";
import "./axiosSetup";

function App() {
    return (
        <Provider store={store}>
            <BrowserRouter>
                <Layout>
                    <ProtectedRoutes />
                </Layout>
            </BrowserRouter>
        </Provider>
    );
}

export default App;
