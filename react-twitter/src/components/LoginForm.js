import React from "react";
import {withRouter} from "react-router-dom";
import {domain} from "../config";


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

    handleChange = (e) => {
        const name = e.target.name;
        const value = e.target.value;
        this.setState({
            [name]: value
        });
    };

    loggingIn = (token) => {
        this.setState({
            token: token,
        });
        localStorage.setItem('user', JSON.stringify(this.state));
        this.props.history.push('/');
    };

    handleSubmit = (e) => {
        fetch(domain + '/news/auth/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: this.state.username,
                password: this.state.password,
            })
        })
            .then((response) => response.json())
            .then((responseJson) => {
                if(responseJson.token)
                    this.loggingIn(responseJson.token);
            })
            .catch((error) => {
                console.error(error);
            });

        e.preventDefault();
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
