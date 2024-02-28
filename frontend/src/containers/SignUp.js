import React, { useState, useEffect } from "react";
import { Link, Navigate } from "react-router-dom";
import { connect } from "react-redux";
import { signup } from "../actions/auth";
import logo from "../static/wespire.png";
import Spinner from "react-bootstrap/Spinner"; // Import Spinner

const Signup = ({ signup, isAuthenticated }) => {
    useEffect(() => {
        document.body.style.background =
            "linear-gradient(to right, rgb(24, 32, 176), rgb(224, 196, 38))";

        return () => {
            document.body.style.background = "none";
        };
    }, []);

    const [accountCreated, setAccountCreated] = useState(false);
    const [formData, setFormData] = useState({
        name: "",
        email: "",
        password: "",
        re_password: "",
    });

    const { name, email, password, re_password } = formData;
    const [loading, setLoading] = useState(false);

    const onChange = (e) =>
        setFormData({ ...formData, [e.target.name]: e.target.value });

    const onSubmit = async (e) => {
        e.preventDefault();

        if (password === re_password) {
            setLoading(true); // Start loading
            await signup(name, email, password, re_password);
            setLoading(false); // Stop loading after signup is complete
            setAccountCreated(true);
        }
    };

    if (isAuthenticated) {
        return <Navigate to="/" />;
    }
    if (accountCreated) {
        return <Navigate to="/login" />;
    }

    return (
        <div className="signup-container">
            <div className="signup-form">
                <img src={logo} alt="logo" className="login-logo" />
                <p>Create your Account</p>
                <form onSubmit={onSubmit}>
                    <div className="form-group">
                        <input
                            type="text"
                            placeholder="Name*"
                            name="name"
                            value={name}
                            onChange={onChange}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <input
                            type="email"
                            placeholder="Email*"
                            name="email"
                            value={email}
                            onChange={onChange}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <input
                            type="password"
                            placeholder="Password*"
                            name="password"
                            value={password}
                            onChange={onChange}
                            minLength="6"
                            required
                        />
                    </div>
                    <div className="form-group">
                        <input
                            type="password"
                            placeholder="Confirm Password*"
                            name="re_password"
                            value={re_password}
                            onChange={onChange}
                            minLength="6"
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
                            "Register"
                        )}
                    </button>
                </form>
                <p className="mt-3">
                    Already have an account? <Link to="/login">Sign In</Link>
                </p>
            </div>
        </div>
    );
};

const mapStateToProps = (state) => ({
    isAuthenticated: state.auth.isAuthenticated,
});

export default connect(mapStateToProps, { signup })(Signup);
