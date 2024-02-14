import React from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import { useSelector } from "react-redux";
import StudentList from "../components/StudentList";
import StudentSummaryList from "../components/StudentSummaryList";
import Login from "../containers/Login";
import SignUp from "../containers/SignUp";
import Activate from "../containers/Activate";
import ResetPassword from "../containers/ResetPassword";
import ResetPasswordConfirm from "../containers/ResetPasswordConfirm";
import Home from "../components/Home";

const ProtectedRoutes = () => {
    const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);

    return (
        <>
            <Routes>
                <Route
                    path="/"
                    element={isAuthenticated ? <Home /> : <Login />}
                />
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<SignUp />} />
                <Route path="/reset-password" element={<ResetPassword />} />
                <Route
                    path="/password/reset/confirm/:uid/:token"
                    element={<ResetPasswordConfirm />}
                />
                <Route path="/activate/:uid/:token" element={<Activate />} />
                {isAuthenticated ? (
                    <>
                        <Route path="/clients" element={<StudentList />} />
                        <Route
                            path="/client-summaries"
                            element={<StudentSummaryList />}
                        />
                    </>
                ) : (
                    <Route path="*" element={<Navigate to="/login" />} />
                )}
            </Routes>
        </>
    );
};

export default ProtectedRoutes;
