import React, { useState, useEffect } from "react";
import { Link, Navigate, useLocation } from "react-router-dom";
import { connect } from "react-redux";
import { login, resendActivationEmail, clearErrors } from "../actions/auth";
import "./Style.css";
import logo from "../static/wespire.png";

const Login = ({
    login,
    isAuthenticated,
    error,
    signUpSuccessEmail,
    resendActivationEmail,
    clearErrors,
}) => {
    const [alertVisible, setAlertVisible] = useState(true);

    const handleCloseAlert = () => {
        clearErrors();
        setAlertVisible(false);
    };

    const location = useLocation();
    const accountVerifiedMessage = location.state?.accountVerified
        ? "Your account has been verified. You can now sign in with your credentials."
        : "";

    useEffect(() => {
        if (error || signUpSuccessEmail) {
            setAlertVisible(true);
        }
    }, [error, signUpSuccessEmail]);
    useEffect(() => {
        document.body.style.background =
            "linear-gradient(to right, rgb(24, 32, 176), rgb(224, 196, 38))";

        return () => {
            document.body.style.background = "none";
            clearErrors();
        };
    }, [clearErrors]);

    const handleResendActivationEmail = () => {
        if (signUpSuccessEmail) {
            resendActivationEmail(signUpSuccessEmail);
        }
    };

    const [formData, setFormData] = useState({
        email: "",
        password: "",
    });

    const { email, password } = formData;

    const onChange = (e) =>
        setFormData({ ...formData, [e.target.name]: e.target.value });

    const onSubmit = async (e) => {
        e.preventDefault();
        login(email, password);
    };

    if (isAuthenticated) {
        return <Navigate to="/" />;
    }

    return (
        <div className="login-container">
            <div className="login-form">
                <form onSubmit={onSubmit}>
                    <img src={logo} alt="logo" className="login-logo" />
                    <h6>Aspire to Inspire</h6>
                    <>
                        {alertVisible && (
                            <>
                                {error ? (
                                    <div
                                        className="alert alert-danger text-center"
                                        role="alert"
                                    >
                                        {error}
                                        <div
                                            style={{
                                                textAlign: "right",
                                                marginTop: "10px",
                                            }}
                                        >
                                            <a
                                                href="#!"
                                                onClick={handleCloseAlert}
                                                style={{
                                                    fontWeight: "bold",
                                                    textDecoration: "underline",
                                                    cursor: "pointer",
                                                }}
                                            >
                                                close
                                            </a>
                                        </div>
                                    </div>
                                ) : accountVerifiedMessage ? (
                                    <div
                                        className="alert alert-success text-center"
                                        role="alert"
                                    >
                                        {accountVerifiedMessage}
                                        <div
                                            style={{
                                                textAlign: "right",
                                                marginTop: "10px",
                                            }}
                                        >
                                            <a
                                                href="#!"
                                                onClick={handleCloseAlert}
                                                style={{
                                                    fontWeight: "bold",
                                                    textDecoration: "underline",
                                                    cursor: "pointer",
                                                }}
                                            >
                                                close
                                            </a>
                                        </div>
                                    </div>
                                ) : signUpSuccessEmail ? (
                                    <div
                                        className="alert alert-success"
                                        role="alert"
                                        style={{
                                            position: "relative",
                                            padding: "1rem 1rem",
                                            marginBottom: "1rem",
                                            border: "1px solid transparent",
                                            borderRadius: ".25rem",
                                        }}
                                    >
                                        <p style={{ margin: 0 }}>
                                            An email has been sent to{" "}
                                            <strong>
                                                {signUpSuccessEmail}
                                            </strong>
                                            , please follow the steps to verify
                                            your account.
                                        </p>
                                        <p style={{ marginTop: "1rem" }}>
                                            If you do not receive the email
                                            within <strong>5 minutes</strong>,
                                            click
                                            <a
                                                href="#!"
                                                onClick={
                                                    handleResendActivationEmail
                                                }
                                                style={{
                                                    marginLeft: "5px",
                                                    fontWeight: "bold",
                                                    textDecoration: "underline",
                                                    cursor: "pointer",
                                                }}
                                            >
                                                here
                                            </a>{" "}
                                            to resend the email.
                                        </p>
                                        <div
                                            style={{
                                                textAlign: "right",
                                                marginTop: "10px",
                                            }}
                                        >
                                            <a
                                                href="#!"
                                                onClick={handleCloseAlert}
                                                style={{
                                                    fontWeight: "bold",
                                                    textDecoration: "underline",
                                                    cursor: "pointer",
                                                }}
                                            >
                                                close
                                            </a>
                                        </div>
                                    </div>
                                ) : null}
                            </>
                        )}
                    </>

                    <div className="form-group">
                        <label htmlFor="email">Email address</label>
                        <input
                            type="email"
                            className="form-control"
                            id="email"
                            name="email"
                            value={email}
                            onChange={onChange}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <input
                            type="password"
                            className="form-control"
                            id="password"
                            name="password"
                            value={password}
                            onChange={onChange}
                            required
                        />
                    </div>
                    <div className="forgot-password">
                        <Link to="/reset-password">Forgot password?</Link>
                    </div>
                    <button type="submit" className="btn btn-primary">
                        Sign In
                    </button>
                    <div className="signup-link">
                        Don't have an account? <Link to="/signup">Sign Up</Link>
                    </div>
                </form>
            </div>
        </div>
    );
};

const mapStateToProps = (state) => ({
    isAuthenticated: state.auth.isAuthenticated,
    error: state.auth.error,
    signUpSuccessEmail: state.auth.signUpSuccessEmail,
});

export default connect(mapStateToProps, {
    login,
    resendActivationEmail,
    clearErrors,
})(Login);
