import React from "react";
import './style.css'
import RegisterForm from "./components/Form";

export default function Register() {
    return(
        <div className="register-container">
            <h1>Faça seu cadastro</h1>
            <RegisterForm/>
        </div>
    )
}