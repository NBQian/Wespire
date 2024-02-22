import React, { useState, useEffect } from "react";
import { connect } from "react-redux";
import { reset_password } from "../actions/auth";
import Spinner from "react-bootstrap/Spinner";
import { Link } from "react-router-dom";

const ResetPassword = ({ reset_password }) => {
    useEffect(() => {
        document.body.style.background =
            "linear-gradient(to right, rgb(24, 32, 176), rgb(224, 196, 38))";

        return () => {
            document.body.style.background = "none";
        };
    }, []);
    const [requestSent, setRequestSent] = useState(false);
    const [email, setEmail] = useState("");
    const [loading, setLoading] = useState(false);

    const onChange = (e) => setEmail(e.target.value);

    const onSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        await reset_password(email);
        setLoading(false);
        setRequestSent(true);
    };

    if (requestSent) {
        return (
            <div className="auth-container">
                <div className="auth-form">
                    <img
                        src={
                            "https://wespirebackend.s3.ap-southeast-1.amazonaws.com/media/wespire.93ec30618e4160b29728.png"
                        }
                        alt="logo"
                        className="auth-logo"
                    />
                    <h2>Check Your Email</h2>
                    <p>
                        An email has been sent to {email}. If it has been
                        registered with us, you will receive the email shortly.
                    </p>
                    <Link to="/login" className="auth-back-link">
                        Back to Sign In
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="auth-container">
            <div className="auth-form">
                <img
                    src={
                        "https://wespirebackend.s3.ap-southeast-1.amazonaws.com/media/wespire.93ec30618e4160b29728.png"
                    }
                    alt="logo"
                    className="auth-logo"
                />
                <p>Enter your email below:</p>
                <form onSubmit={onSubmit}>
                    <div className="form-group">
                        <input
                            type="email"
                            placeholder="Email"
                            name="email"
                            value={email}
                            onChange={onChange}
                            required
                            disabled={loading}
                        />
                    </div>
                    <button type="submit" disabled={loading}>
                        {loading ? (
                            <>
                                <Spinner
                                    animation="border"
                                    size="sm"
                                    role="status"
                                    aria-hidden="true"
                                />
                                <span> Loading...</span>
                            </>
                        ) : (
                            "Reset Password"
                        )}
                    </button>
                </form>
                <Link to="/login" className="auth-back-link">
                    Back to Sign In
                </Link>
            </div>
        </div>
    );
};

export default connect(null, { reset_password })(ResetPassword);
