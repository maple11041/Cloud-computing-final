import React, { useState } from "react";
import NavBar from "./components/NavBar";
import LoginForm from "./components/LoginForm";
import SignUpForm from "./components/SignUpForm";
import ImageUpload from "./components/ImageUpload";
import GanUpload from "./components/GanUpload";
import Result from "./components/Result";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import "./App.css";

function App() {
    const [token, setToken] = useState("");
    return (
        <Router>
            <>
                <NavBar token={token} />
                <Switch>
                    <Route
                        path="/"
                        exact
                        component={() => <LoginForm setToken={setToken} />}
                    />
                    <Route path="/signup" component={SignUpForm} />
                    <Route path="/upload" component={ImageUpload} />
                    <Route path="/GanUpload" component={GanUpload} />
                </Switch>
            </>
        </Router>
    );
}

export default App;
