import React, { Component } from "react";

import { RegisterForm } from "./Form/RegisterForm";

import { api } from "../.././utils/api";

export class Register extends Component {
  state = {
    institutions: []
  };
  submitRegisterForm = event => {
    event.preventDefault();
    const {
      target: { elements }
    } = event;
    const data = {
      email: elements.email.value,
      username: elements.username.value,
      password: elements.password.value
    };
    api
      .post(`register/`, data)
      .then(({ data }) => {
        this.props.history.push(`/login`);
      })
      .catch(error => {
        console.log("error", error.message);
        // todo show toast
      });
  };
  render() {
    return <RegisterForm submitForm={this.submitRegisterForm} />;
  }
}
