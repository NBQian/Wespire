import React, { useEffect } from "react";
import { useSelector } from "react-redux";
import Navigation from "../components/Navigation";
import { checkAuthenticated, load_user } from "../actions/auth";
import { connect } from "react-redux";
import { Navigate } from "react-router-dom";

const Layout = ({ checkAuthenticated, load_user, children }) => {
    const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);

    useEffect(() => {
        checkAuthenticated();
        load_user();
    }, []);

    // if (!isAuthenticated) {
    //     return <Navigate to="/login" />;
    // }

    return (
        <div>
            {isAuthenticated && <Navigation />}
            {children}
        </div>
    );
};

export default connect(null, { checkAuthenticated, load_user })(Layout);
