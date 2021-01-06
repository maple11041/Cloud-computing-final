import React from "react";
import NavBar from "./components/NavBar";
import LoginForm from "./components/LoginForm";
import SignUpForm from "./components/SignUpForm";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import "./App.css";

function App() {
    return (
        <Router>
            <>
                <NavBar />
                <Switch>
                    <Route path="/" exact component={LoginForm} />
                    <Route path="/signup" component={SignUpForm} />
                </Switch>
            </>
        </Router>
    );
}

export default App;
