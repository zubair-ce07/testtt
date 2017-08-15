import React from 'react';
import {Bootstrap, Col, Button, Image, FormGroup} from 'react-bootstrap';

class SignUp extends React.Component{
    render() {
        return(
            <div className="container-fluid main-container">
                <div className="container signup">
                    <div className="col-md-6 col-sm-12">
                        <h1> </h1>
                    </div>
                    <SignUpPanel/>
                </div>
                <div className="col-md-6 col-sm-12">
                    <h1> </h1>
                </div>
                <div className="col-lg-4 col-md-4 col-sm-12 col-xs-12 get-app">
                    <img
                        className="center-block get-app-logo"
                        src={require("../static/images/app-store.png")}
                    />
                    <img
                        className="center-block get-app-logo"
                        src={require("../static/images/play-store.png")}
                    />
                </div>
            </div>
        )
    }
}

class SignUpPanel extends React.Component{
    render() {
        return(
            <div>
                <div className="col-lg-4 col-md-4 col-sm-12 signup-form-panel">
                    <div className="insta-logo-text">
                        <img
                            className="center-block signup-logo"
                            src={require("../static/images/logo.png")}
                        />
                        <h4 className="text-center signup-text-under-logo">
                            <strong>
                                Sign up to see photos and videos from your friends
                            </strong>
                        </h4>
                        <img
                            className="center-block"
                            src={require("../static/images/login-facebook.png")}
                        /> <br/>
                        <SignUpForm/> <br/>
                        <h5 className="text-center signup-text-under-logo">
                            By signing up, you agree to our
                            <strong> Terms</strong> &
                            <strong> Privacy Policy</strong>.
                        </h5>
                    </div>
                </div>
                <div className="col-md-6 col-sm-12">
                    <h1> </h1>
                </div>
                <div className="signup-form-panel-2">
                    <div className="col-lg-4 col-md-4 col-sm-12 signup-form-panel">
                        <div className="text-center signup-switch">
                            <h5>
                                Have an account? <button
                                                    type="button"
                                                    className="btn btn-link signup-btn-switch">Login</button>
                            </h5>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

class SignUpForm extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            isValid: false
        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleInputChange = this.handleInputChange.bind(this);
    }

    handleInputChange(event){
        const name = event.target.name;
        const value = event.target.value;

        this.setState({
            [name]: value
        });
        console.log(event.target.name, event.target.value);
        if(name === "email" || name === "username") {
            fetch('http://127.0.0.1:8000/api/signup/available/', {
                method: 'post',
                body: JSON.stringify({
                    [name]: event.target.value
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(function (response) {
                return response.json()
            }).then(function (data) {
                console.log(data.is_taken);
                const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
                if(data.is_taken === true || value.length < 1) {
                    if(name === 'email'){
                        document.styleSheets[1]['rules'][11].style.borderColor =
                        "rgb(255, 51, 51)"
                    } else {
                        document.styleSheets[1]['rules'][12].style.borderColor =
                            "rgb(255, 51, 51)"
                    }
                } else if(name === 'email') {
                    if(re.test(value) === false){
                        document.styleSheets[1]['rules'][11].style.borderColor =
                        "rgb(255, 51, 51)"
                    } else {
                        document.styleSheets[1]['rules'][11].style.borderColor =
                            "rgb(0, 204, 102)"
                    }
                } else {
                    document.styleSheets[1]['rules'][12].style.borderColor =
                        "rgb(0, 204, 102)";
                }
            }).catch(function (error) {
                console.log(error)
            });
        } else if(name === "first_name"){// || name === "last_name"){
            if(value.length <2) {
                document.styleSheets[1]['rules'][13].style.borderColor =
                            "rgb(255, 51, 51)"
            } else {
                document.styleSheets[1]['rules'][13].style.borderColor =
                        "rgb(0, 204, 102)";
            }
        } else if(name === "last_name"){// || name === "last_name"){
            if(value.length <2) {
                document.styleSheets[1]['rules'][14].style.borderColor =
                            "rgb(255, 51, 51)"
            } else {
                document.styleSheets[1]['rules'][14].style.borderColor =
                        "rgb(0, 204, 102)";
            }
        } else if(name === "password"){// || name === "last_name"){
            if(value.length < 5) {
                document.styleSheets[1]['rules'][15].style.borderColor =
                            "rgb(255, 51, 51)"
            } else {
                document.styleSheets[1]['rules'][15].style.borderColor =
                        "rgb(0, 204, 102)";
            }
        } else if(name === "date_of_birth"){// || name === "last_name"){
            console.log(value)
            if(value.length <2) {
                document.styleSheets[1]['rules'][16].style.borderColor =
                            "rgb(255, 51, 51)"
            } else {
                document.styleSheets[1]['rules'][16].style.borderColor =
                        "rgb(0, 204, 102)";
            }
        }


    }

    handleSubmit(event){
        console.log(this.state.email);
        event.preventDefault()
    //    validate data
    //    fetch api here and send data
    }

    render(){
        return(
            <div className="signup-form text-center">
            <form className="text-center" onSubmit={this.handleSubmit}>
                <div className="form-group signup-field">
                    <input
                        className="form-control email"
                        name="email"
                        type="text"
                        placeholder="Email Address"
                        onChange={this.handleInputChange}
                    /> <br/>
                </div>
                <div className="form-group signup-field first_name">
                    <input
                        className="form-control first-name"
                        name="first_name"
                        type="text"
                        placeholder="First Name"
                        onChange={this.handleInputChange}
                    /> <br/>
                </div>
                <div className="form-group signup-field">
                    <input
                        className="form-control last-name"
                        name="last_name"
                        type="text"
                        placeholder="Last Name"
                        onChange={this.handleInputChange}
                    /> <br/>
                </div>
                <div className="form-group signup-field">
                    <input
                        className="form-control username"
                        name="username"
                        type="text"
                        placeholder="Username"
                        onChange={this.handleInputChange}
                    /> <br/>
                </div>
                <div className="form-group signup-field">
                    <input
                        className="form-control password"
                        name="password"
                        type="password"
                        placeholder="Password"
                        onChange={this.handleInputChange}
                    /> <br/>
                </div>
                <div className="form-group signup-field">
                    <input
                        className="form-control date-of-birth"
                        name="date_of_birth"
                        type="date"
                        onChange={this.handleInputChange}
                    /> <br/>
                </div>
                <button type="submit" className="btn btn-submit" onClick={this.handleSubmit}><strong>Submit</strong></button>
            </form>
            </div>
        )
    }
}

// /home/humdah/React/insta/src/insta/static/images/logo.png
export default SignUp;