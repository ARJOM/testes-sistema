import React from "react";
import { Formik, Field, Form } from 'formik';
import './style.css'
import api from "../../../../../services/api";


export default function RegisterForm() {
    return (
        <Formik
            initialValues={{ email: '', user_name: '', birthday: '', gender: 1, password: ''}}
            onSubmit={async (values) => {
                try {
                    await api.post('users', values);
                    alert("Cadastro realizado com sucesso");
                } catch (e) {
                    alert("Já existe um usuário registrado com esse email")
                }
            }}
        >
            <Form className={"cadastro"}>
                <label htmlFor="email">Email</label>
                <Field name="email" type="email" placeholder="Ex: jose@gmail.com"/>

                <label htmlFor="user_name">Nome</label>
                <Field name="user_name" type="text" placeholder="Ex: João da Silva"/>

                <label htmlFor="birthday">Data de Nascimento</label>
                <Field name="birthday" type="date"/>

                <label htmlFor="password">Senha</label>
                <Field name="password" type="password" placeholder="*********"/>

                <label htmlFor="gender">Gênero</label>
                <Field name="gender" as={"select"}>
                    <option value={1}>Masculino</option>
                    <option value={2}>Feminino</option>
                    <option value={3}>Outro</option>
                </Field>

                <button type={"submit"}>Registrar</button>
            </Form>
        </Formik>
    )

}