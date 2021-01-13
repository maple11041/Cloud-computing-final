import React from "react";
import NavBar from "./components/NavBar";
import LoginForm from "./components/LoginForm";
import SignUpForm from "./components/SignUpForm";
import ImageUpload from "./components/ImageUpload";
import GanUpload from "./components/GanUpload";
import Result from "./components/Result";
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
                    <Route path="/upload" component={ImageUpload} />
                    <Route path="/GanUpload" component={GanUpload} />
                </Switch>
            </>
        </Router>
    );
}

export default App;
