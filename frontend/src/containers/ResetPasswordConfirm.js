import React, { useState, useEffect } from "react";
import { useParams, Navigate } from "react-router-dom";
import { connect } from "react-redux";
import { reset_password_confirm } from "../actions/auth";
import Spinner from "react-bootstrap/Spinner";
import logo from "../static/wespire.png";

const ResetPasswordConfirm = ({ reset_password_confirm }) => {
    const [requestSent, setRequestSent] = useState(false);
    const [passwordError, setPasswordError] = useState("");
    const [formData, setFormData] = useState({
        new_password: "",
        re_new_password: "",
    });
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false); // New state for tracking success

    const { new_password, re_new_password } = formData;
    const { uid, token } = useParams();

    useEffect(() => {
        document.body.style.background =
            "linear-gradient(to right, rgb(24, 32, 176), rgb(224, 196, 38))";

        return () => {
            document.body.style.background = "none";
        };
    }, []);

    const onChange = (e) => {
        setPasswordError("");
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const onSubmit = async (e) => {
        e.preventDefault();

        if (new_password.length < 8 || re_new_password.length < 8) {
            setPasswordError("Passwords must be at least 8 characters long.");
            return;
        }

        if (new_password !== re_new_password) {
            setPasswordError("The passwords do not match.");
            return;
        }

        setLoading(true);
        await reset_password_confirm(uid, token, new_password, re_new_password);
        setLoading(false);
        setSuccess(true); // Indicate success

        setTimeout(() => {
            setRequestSent(true);
        }, 500); // Delay the redirection by 0.5 seconds
    };

    if (requestSent) {
        return <Navigate to="/" />;
    }

    return (
        <div className="login-container">
            <div className="auth-form">
                <img src={logo} alt="logo" className="login-logo" />
                <p>Set a new password:</p>
                {passwordError && (
                    <div
                        className="alert alert-danger text-center"
                        role="alert"
                    >
                        {passwordError}
                    </div>
                )}
                <form onSubmit={onSubmit}>
                    <div className="form-group">
                        <input
                            className="form-control"
                            type="password"
                            placeholder="New Password"
                            name="new_password"
                            value={new_password}
                            onChange={onChange}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <input
                            className="form-control"
                            type="password"
                            placeholder="Confirm New Password"
                            name="re_new_password"
                            value={re_new_password}
                            onChange={onChange}
                            required
                        />
                    </div>
                    <button
                        type="submit"
                        disabled={loading || success}
                        style={{
                            backgroundColor: success ? "green" : "",
                            color: success ? "#FFFFFF" : "",
                        }}
                    >
                        {loading ? (
                            <>
                                <Spinner
                                    as="span"
                                    animation="border"
                                    size="sm"
                                    role="status"
                                    aria-hidden="true"
                                    style={{ marginRight: "10px" }}
                                />
                                <span>Loading...</span>
                            </>
                        ) : success ? (
                            "Success!"
                        ) : (
                            "Reset Password"
                        )}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default connect(null, { reset_password_confirm })(ResetPasswordConfirm);
