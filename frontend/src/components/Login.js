import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    let navigate = useNavigate();

    const handleLogin = async (event) => {
        event.preventDefault();
        // Perform the login request to the Django backend
        const response = await fetch("/path/to/your/django/login/view/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                // Additional headers if needed
            },
            body: JSON.stringify({ username, password }),
            credentials: "include", // If you're using cookies for sessions
        });

        if (response.ok) {
            // If login was successful, redirect to the home page
            navigate("/");
        } else {
            // If there was an error, handle it here
            alert("Login failed. Please check your username and password.");
        }
    };

    return (
        <form onSubmit={handleLogin}>
            <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
            />
            <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
            />
            <button type="submit">Login</button>
        </form>
    );
};

export default Login;
