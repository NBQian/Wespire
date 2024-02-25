import React, { useState, useEffect } from "react";
import { Navigate, useParams } from "react-router-dom";
import { connect } from "react-redux";
import { verify } from "../actions/auth";
import logo from "../static/wespire.png";

const Activate = ({ verify }) => {
    useEffect(() => {
        document.body.style.background =
            "linear-gradient(to right, rgb(24, 32, 176), rgb(224, 196, 38))";

        return () => {
            document.body.style.background = "none";
        };
    }, []);
    const [verified, setVerified] = useState(false);
    const { uid, token } = useParams();

    const verify_account = () => {
        verify(uid, token);
        setVerified(true);
    };

    if (verified) {
        return <Navigate to="/" />;
    }

    return (
        <div className="auth-container">
            <div className="auth-form">
                <img src={logo} alt="logo" className="auth-logo" />
                <p>click the button below to verify your account:</p>
                <button onClick={verify_account} className="btn-verify">
                    Verify Account
                </button>
            </div>
        </div>
    );
};

export default connect(null, { verify })(Activate);
