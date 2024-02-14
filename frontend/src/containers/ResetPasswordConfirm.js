import React, { useState } from "react";
import { useParams, Navigate } from "react-router-dom";
import { connect } from "react-redux";
import { reset_password_confirm } from "../actions/auth";

const ResetPasswordConfirm = ({ reset_password_confirm }) => {
    const [requestSent, setRequestSent] = useState(false);
    const [passwordError, setPasswordError] = useState("");
    const [formData, setFormData] = useState({
        new_password: "",
        re_new_password: "",
    });

    const { new_password, re_new_password } = formData;
    const { uid, token } = useParams();

    const onChange = (e) => {
        setPasswordError(""); // Reset password error on input change
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const onSubmit = (e) => {
        e.preventDefault();

        // Check if the password length is at least 8 characters
        if (new_password.length < 8 || re_new_password.length < 8) {
            setPasswordError("Passwords must be at least 8 characters long.");
            return;
        }

        reset_password_confirm(uid, token, new_password, re_new_password);
        setRequestSent(true);
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
                <button className="btn btn-primary" type="submit">
                    Reset Password
                </button>
            </form>
        </div>
    );
};

export default connect(null, { reset_password_confirm })(ResetPasswordConfirm);
