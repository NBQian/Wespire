import React, { useState } from "react";
import { useParams, Navigate } from "react-router-dom";
import { connect } from "react-redux";
import { reset_password_confirm } from "../actions/auth";
import Spinner from "react-bootstrap/Spinner"; // Import Spinner

const ResetPasswordConfirm = ({ reset_password_confirm }) => {
    const [requestSent, setRequestSent] = useState(false);
    const [passwordError, setPasswordError] = useState("");
    const [formData, setFormData] = useState({
        new_password: "",
        re_new_password: "",
    });
    const [loading, setLoading] = useState(false);

    const { new_password, re_new_password } = formData;
    const { uid, token } = useParams();

    const onChange = (e) => {
        setPasswordError(""); // Reset password error on input change
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const onSubmit = async (e) => {
        e.preventDefault();
        if (new_password === re_new_password && new_password.length >= 8) {
            setLoading(true); // Start loading
            await reset_password_confirm(
                uid,
                token,
                new_password,
                re_new_password
            );
            setLoading(false); // Stop loading after signup is complete
            setRequestSent(true);
        }
        // Check if the password length is at least 8 characters
        if (new_password.length < 8 || re_new_password.length < 8) {
            setPasswordError("Passwords must be at least 8 characters long.");
            return;
        }

        if (new_password !== re_new_password) {
            setPasswordError("The passwords do not match.");
            return;
        }
    };

    if (requestSent) {
        return <Navigate to="/" />;
    }

    return (
        <div className="container mt-5">
            <h1>Confirm Password Reset:</h1>
            {passwordError && (
                <div className="alert alert-danger" role="alert">
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
                <button type="submit" disabled={loading}>
                    {loading ? (
                        <>
                            <Spinner
                                as="span"
                                animation="border"
                                size="sm"
                                role="status"
                                aria-hidden="true"
                            />
                            <span className="ml-2">Loading...</span>
                        </>
                    ) : (
                        "Reset Password"
                    )}
                </button>
            </form>
        </div>
    );
};

export default connect(null, { reset_password_confirm })(ResetPasswordConfirm);
