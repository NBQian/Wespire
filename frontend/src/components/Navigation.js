import React from "react";
import { Navbar, Nav, Container } from "react-bootstrap";
import { NavLink, useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { logout } from "../actions/auth";
import "../App.css";

// The Lord is my Light. I shall not want.

const Navigation = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const handleLogout = () => {
        dispatch(logout());
        navigate("/login");
    };

    return (
        <Navbar className="gradient-dark-bg" variant="dark" id="my-nav">
            <Container fluid>
                <Navbar.Brand as={NavLink} to="/" end>
                    <img
                        src={
                            "https://wespirebackend.s3.ap-southeast-1.amazonaws.com/media/wespire.93ec30618e4160b29728.png"
                        }
                        width="140"
                        height="35"
                        className="d-inline-block align-top"
                        alt="Logo"
                    />
                </Navbar.Brand>

                <Nav className="me-auto">
                    <Nav.Link
                        as={NavLink}
                        to="/"
                        end
                        className="d-flex align-items-center me-4"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="25"
                            height="25"
                            fill="currentColor"
                            class="bi bi-house-door-fill me-2"
                            viewBox="0 0 16 16"
                        >
                            <path d="M6.5 14.5v-3.505c0-.245.25-.495.5-.495h2c.25 0 .5.25.5.5v3.5a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5v-7a.5.5 0 0 0-.146-.354L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293L8.354 1.146a.5.5 0 0 0-.708 0l-6 6A.5.5 0 0 0 1.5 7.5v7a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5" />
                        </svg>
                        <span className="d-none d-sm-inline">Home</span>
                    </Nav.Link>

                    <Nav.Link
                        as={NavLink}
                        exact
                        to="/clients"
                        className="d-flex align-items-center me-4"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="25"
                            height="25"
                            fill="currentColor"
                            class="bi bi-person-lines-fill me-2"
                            viewBox="0 0 16 16"
                        >
                            <path d="M6 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6m-5 6s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1zM11 3.5a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 0 1h-4a.5.5 0 0 1-.5-.5m.5 2.5a.5.5 0 0 0 0 1h4a.5.5 0 0 0 0-1zm2 3a.5.5 0 0 0 0 1h2a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h2a.5.5 0 0 0 0-1z" />
                        </svg>
                        <span className="d-none d-sm-inline">Clients</span>
                    </Nav.Link>

                    <Nav.Link
                        as={NavLink}
                        exact
                        to="/client-summaries"
                        className="d-flex align-items-center"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="25"
                            height="25"
                            fill="currentColor"
                            class="bi bi-file-earmark-medical-fill me-2"
                            viewBox="0 0 16 16"
                            style={{ verticalAlign: "middle" }}
                        >
                            <path d="M9.293 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.707A1 1 0 0 0 13.707 4L10 .293A1 1 0 0 0 9.293 0M9.5 3.5v-2l3 3h-2a1 1 0 0 1-1-1m-3 2v.634l.549-.317a.5.5 0 1 1 .5.866L7 7l.549.317a.5.5 0 1 1-.5.866L6.5 7.866V8.5a.5.5 0 0 1-1 0v-.634l-.549.317a.5.5 0 1 1-.5-.866L5 7l-.549-.317a.5.5 0 0 1 .5-.866l.549.317V5.5a.5.5 0 1 1 1 0m-2 4.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1 0-1m0 2h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1 0-1" />
                        </svg>
                        <span className="d-none d-sm-inline">Summaries</span>
                    </Nav.Link>
                </Nav>
                <Nav>
                    <Nav.Link
                        onClick={handleLogout}
                        style={{ display: "flex", alignItems: "center" }}
                        className="d-flex align-items-center"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="25"
                            height="25"
                            fill="currentColor"
                            class="bi bi-box-arrow-right me-2"
                            viewBox="0 0 16 16"
                        >
                            <path
                                fill-rule="evenodd"
                                d="M10 12.5a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v2a.5.5 0 0 0 1 0v-2A1.5 1.5 0 0 0 9.5 2h-8A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-2a.5.5 0 0 0-1 0z"
                            />
                            <path
                                fill-rule="evenodd"
                                d="M15.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L14.293 7.5H5.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708z"
                            />
                        </svg>
                        <span
                            style={{
                                display: "inline-block",
                                marginTop: "2px",
                            }}
                        >
                            <span className="d-none d-sm-inline me-4">
                                Logout
                            </span>
                        </span>
                    </Nav.Link>
                </Nav>
            </Container>
        </Navbar>
    );
};

export default Navigation;
