import React from "react";
import { Navbar, Nav, Container } from "react-bootstrap";
import { NavLink, useNavigate } from "react-router-dom";
import logo from "../static/wespire.png";
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
                        src={logo}
                        width="140"
                        height="35"
                        className="d-inline-block align-top"
                        alt="Logo"
                    />
                </Navbar.Brand>

                <Nav className="me-auto">
                    <Nav.Link as={NavLink} to="/" end>
                        <i className="bi bi-house-door-fill fs-4 me-2"></i>
                        <span className="d-none d-sm-inline me-4">Home</span>
                    </Nav.Link>

                    <Nav.Link as={NavLink} exact to="/clients">
                        <i className="bi bi-person-lines-fill fs-4 me-2"></i>
                        <span className="d-none d-sm-inline me-4">Clients</span>
                    </Nav.Link>
                    <Nav.Link as={NavLink} exact to="/client-summaries">
                        <i className="bi bi-file-earmark-medical-fill fs-4 me-2"></i>
                        <span className="d-none d-sm-inline">Summaries</span>
                    </Nav.Link>
                </Nav>
                <Nav>
                    <Nav.Link
                        onClick={handleLogout}
                        style={{ display: "flex", alignItems: "center" }}
                    >
                        <i className="bi bi-box-arrow-right fs-4 me-2"></i>
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
