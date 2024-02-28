import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { connect } from "react-redux";
import { verify } from "../actions/auth";
import Spinner from "react-bootstrap/Spinner"; // Make sure to import Spinner from your UI library
import logo from "../static/wespire.png"; // Assuming this path is correct

const Activate = ({ verify }) => {
    const navigate = useNavigate();
    const { uid, token } = useParams();
    const [loading, setLoading] = useState(true); // State to manage loading state

    useEffect(() => {
        document.body.style.background =
            "linear-gradient(to right, rgb(24, 32, 176), rgb(224, 196, 38))";

        verify(uid, token).then(() => {
            setLoading(false); // Stop loading once the verification is done
            navigate("/login", { state: { accountVerified: true } });
        });

        return () => {
            document.body.style.background = "none";
        };
    }, [verify, uid, token, navigate]);

    return (
        <div className="auth-container">
            <div className="auth-form text-center">
                <img src={logo} alt="logo" className="auth-logo mb-3" />
                {loading ? (
                    <>
                        <p>Verifying...</p>
                        <Spinner animation="border" role="status">
                            <span className="visually-hidden">Loading...</span>
                        </Spinner>
                    </>
                ) : null}
            </div>
        </div>
    );
};

export default connect(null, { verify })(Activate);
