import React, { useState } from "react";
import axios from "axios";
import { Redirect } from "react-router-dom";
import { Button, Form } from "react-bootstrap";
import "./LoginForm.css";

const API_URL = "http://localhost:5000";

const LoginForm = ({ setToken }) => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [warning, setWarning] = useState("");
    const [ifToken, setIfToken] = useState(false);

    const login = async () => {
        try {
            const payload = {
                email: email,
                password: password,
            };
            const response = await axios.post(
                `${API_URL}/api/user/login`,
                payload
            );
            if (response.data.success) {
                localStorage.setItem("token", response.data.token);
                setIfToken(true);
                setToken(response.data.token);
            } else {
                setWarning(response.data.message);
            }
        } catch (error) {
            console.log(error);
        }
    };

    const handleLogin = (ev) => {
        ev.preventDefault();
        if (email.length > 0 && password.length > 6) {
            login();
            setEmail("");
            setPassword("");
        } else {
            setWarning("Name and password should be longer than 6 characters");
        }
    };

    if (ifToken) {
        // window.location.reload(false);
        return <Redirect to="/upload" />;
    }
    return (
        <div className="login-form">
            <Form style={{ width: "30%" }} onSubmit={handleLogin}>
                <Form.Group controlId="formBasicEmail">
                    <Form.Label>Email address</Form.Label>
                    <Form.Control
                        type="email"
                        placeholder="Enter email"
                        onChange={(ev) => setEmail(ev.target.value)}
                        value={email}
                    />
                </Form.Group>

                <Form.Group controlId="formBasicPassword">
                    <Form.Label>Password</Form.Label>
                    <Form.Control
                        type="password"
                        placeholder="Password"
                        onChange={(ev) => setPassword(ev.target.value)}
                        value={password}
                    />
                </Form.Group>

                <Button variant="primary" type="submit">
                    Login
                </Button>
                <span className="warning">{warning}</span>
            </Form>
        </div>
    );
};

export default LoginForm;
