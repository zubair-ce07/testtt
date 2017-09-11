import React from "react";
import {withRouter} from "react-router-dom";
import {domain, getHeader} from "../config";


class LoginForm extends React.Component {
    static isPrivate = false;
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: '',
            token: '',
        };
    }

    handleChange = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        this.setState({
            [name]: value
        });
    };

    tryLogIn = (token) => {
        if (token) {
            this.setState({
                token: token,
            });
            localStorage.setItem('user', JSON.stringify(this.state));
        }
        else {
            alert("Username or password is incorrect!")
        }
        this.props.history.push('/');
    };

    handleSubmit = (event) => {
        fetch(domain + '/news/auth/', {
            method: 'POST',
            headers: getHeader(),
            body: JSON.stringify({
                username: this.state.username,
                password: this.state.password,
            }),
        })
            .then(response => response.json())
            .then(responseJson => this.tryLogIn(responseJson.token))
            .catch((error) => {
                console.log(error);
            });

        event.preventDefault();
    };

    render() {
        return (
            <div name="loginForm" className="loginForm">
                <h2>Please Login</h2>
                <form onSubmit={this.handleSubmit}>
                    <input type="text" name="username" placeholder="username" value={this.state.username}
                           onChange={this.handleChange}/>
                    <br/>
                    <input type="password" name="password" placeholder="password" value={this.state.password}
                           onChange={this.handleChange}/>
                    <br/>
                    <input type="submit" value="submit"/>
                </form>
            </div>
        )
    }
}

export default withRouter(LoginForm);
