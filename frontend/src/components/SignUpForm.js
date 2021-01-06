import React, { useState } from "react";
import axios from "axios";
import { Button, Form } from "react-bootstrap";
import "./SignUpForm.css";

const API_URL = "http://localhost:5000";

const SignUpForm = () => {
    const [email, setEmail] = useState("");
    const [name, setName] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPW, setConfirmPW] = useState("");
    const [warning, setWarning] = useState("");

    const clearField = () => {
        setEmail("");
        setName("");
        setPassword("");
        setConfirmPW("");
    };

    const validate = () => {
        if (email.length === 0) {
            setWarning("Email is required");
            return false;
        } else if (name.length <= 6 && password.length <= 6) {
            setWarning("Name and password should be longer than 6 characters");
            return false;
        } else if (confirmPW !== password) {
            setWarning("Two password are different");
            return false;
        } else {
            return true;
        }
    };

    const signUp = async (ev) => {
        ev.preventDefault();
        if (validate(email, name, password)) {
            try {
                const payload = {
                    email: email,
                    username: name,
                    password: password,
                };
                const response = await axios.post(
                    `${API_URL}/api/user/register`,
                    payload
                );
                if (response.data.success) {
                    localStorage.removeItem("token");
                    setWarning("");
                    window.location.href = "/";
                } else {
                    setWarning(response.data.message);
                }
            } catch (error) {
                console.log(error);
            }
            clearField();
        }
    };

    return (
        <div className="signup-form" onSubmit={signUp}>
            <Form style={{ width: "30%" }}>
                <Form.Group controlId="formBasicName">
                    <Form.Label>Name</Form.Label>
                    <Form.Control
                        placeholder="Enter your name"
                        onChange={(ev) => setName(ev.target.value)}
                        value={name}
                    />
                </Form.Group>
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

                <Form.Group controlId="formBasicPassword">
                    <Form.Label>Confirm Password</Form.Label>
                    <Form.Control
                        type="password"
                        placeholder="Password"
                        onChange={(ev) => setConfirmPW(ev.target.value)}
                        value={confirmPW}
                    />
                </Form.Group>
                <Button variant="primary" type="submit">
                    Sign Up
                </Button>
                <span className="warning">{warning}</span>
            </Form>
        </div>
    );
};

export default SignUpForm;
