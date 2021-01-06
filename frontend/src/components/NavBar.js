import React, { useState } from "react";
import { Navbar, Nav } from "react-bootstrap";

const NavBar = () => {
    // disable home and history if token is not present
    // disable login if token is present
    const ifToken = localStorage.getItem("token") === null;
    const logout = () => {
        // remove token only if signed in
        if (!ifToken) {
            localStorage.removeItem("token");
        }
    };
    // switch text for link
    const inOut = ifToken ? "Login" : "Logout";
    return (
        <Navbar bg="light" expand="lg">
            <Navbar.Brand href="/home">Cloud Computing</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mr-auto">
                    <Nav.Link href="/home">Home</Nav.Link>
                    <Nav.Link href="/" onClick={logout}>
                        {inOut}
                    </Nav.Link>
                    <Nav.Link href="/signup">Sign Up</Nav.Link>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    );
};

export default NavBar;
