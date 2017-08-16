import React from 'react';
import validateUsernameEmail from '../utils/validate/usernameEmail'
import validateNamePasswordDOB from '../utils/validate/namePasswordDOB'


class SignUp extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            isSignup: true
        };
        this.switchPanel = this.switchPanel.bind(this);
    }

    switchPanel() {
        this.setState({
            isSignup: !this.state.isSignup
        });
    }

    render() {
        return(
            <div className="container-fluid col-lg-12 col-md-12 col-sm-12 main-container">
                <div className="container signup">
                    <div className="col-md-6 visible-lg">
                        <PhonePanel/>
                    </div>
                    {/*{this.state.panel}*/}
                    {this.state.isSignup ?
                        <SignUpPanel switchParentPanel={this.switchPanel}/>
                        :
                        <LoginPanel switchParentPanel={this.switchPanel}/>
                    }
                </div>
            </div>
        )
    }
}

class AppIcons extends React.Component{
    render() {
        return(
            <div>
                <div className="col-md-6 col-sm-12">
                    <h1> </h1>
                </div>
                <div className="col-md-4 col-sm-12">
                    <br/>
                    <p className="text-center"> Get the app. </p>
                </div>

                <div className="col-md-6 col-sm-12">
                    <h1> </h1>
                </div>
                <div className=" col-md-1 col-sm-6 get-app">
                    <img
                        className="center-block get-app-logo"
                        src={require("../static/images/app-store.png")}
                    />
                </div>
                <div className=" col-md-1 col-sm-6 get-app">
                    <img
                        className="center-block get-app-logo"
                        src={require("../static/images/play-store.png")}
                    />
                </div>
            </div>
        )
    }
}

class LoginPanel extends React.Component{
    render() {
        return(
            <div>
                <div className="col-lg-4 col-md-4 col-sm-12 login-form-panel">
                    <div className="insta-logo-text">
                        <img
                            className="center-block signup-logo"
                            src={require("../static/images/logo.png")}
                        />
                        <LogInForm/> <br/>
                    </div>
                </div>
                <div className="col-md-6 col-sm-12">
                    <h1> </h1>
                </div>
                <div className="signup-form-panel-2">
                    <div className="col-lg-4 col-md-4 col-sm-12 login-form-panel-two">
                        <div className="text-center signup-switch">
                            <h5>
                                Don't have an account?
                                <button
                                    type="button"
                                    onClick={this.props.switchParentPanel}
                                    className="btn btn-link signup-btn-switch">
                                    Sign up
                                </button>
                            </h5>
                        </div>
                    </div>
                </div>
                <AppIcons/>
            </div>
        )
    }
}

class LogInForm extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            isValidUsername: false,
            isValidPassword: false,
        }
        // this.handleSubmit = this.handleSubmit.bind(this);
        this.handleInputChange = this.handleInputChange.bind(this);
    }

    handleInputChange(event){
        const name = event.target.name;
        const value = event.target.value;

        console.log(name, value)

        this.setState({
            [name]: value
        });
        if(name === "username") {
            debugger;
            if(value.length < 1){
                this.setState({
                    isValidPassword: false,
                })
            console.log(':3')
            } else {
                console.log(':>')
                this.setState({
                    isValidPassword: true,
                })
            }
            console.log(this.state.isValidUsername)
        } else if(name === "password"){
            // let isValid = validateNamePasswordDOB(value, 15, 5);
            if(value.length < 5){
                this.setState({
                    isValidPassword: false,
                })
            } else {
                this.setState({
                    isValidPassword: true,
                })
            }
        }
    }

    render(){
        return(
            <div className="signup-form text-center">
            <form className="text-center" onSubmit={this.handleSubmit}>
                <div className="form-group signup-field">
                    <input
                        className="form-control login-username"
                        name="username"
                        type="text"
                        placeholder="Username"
                        onChange={this.handleInputChange}
                    /> <br/>
                </div>
                <div className="form-group signup-field">
                    <input
                        className="form-control login-password"
                        name="password"
                        type="password"
                        placeholder="Password"
                        onChange={this.handleInputChange}
                    /> <br/>
                </div>
                <button
                    type="submit"
                    className="btn btn-submit"
                    onClick={this.handleSubmit}>
                    <strong>Login</strong>
                </button>
            </form>
                <br/>
                <a className="text-center forgot-password" href="/">Forgot password?</a>
            </div>
        )
    }
}

class PhonePanel extends React.Component{
    // constructor(props){
    //     super(props);
    //     this.baseImagePath = "../static/images/";
    //     this.allImages = ["1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg"]
    //     this.state = {
    //         currentImage: "../static/images/1.jpg",
    //         currentIndex: 0,
    //     }
    // }
    //
    // componentDidMount(){
    //     // setInterval(
    //     //     () => this.changeImage(),
    //     //     2000
    //     // );
    //     // console.log(this.baseImagePath+this.state.currentImage)
    // }

    render() {
        return(
            <div>
                <div className="parent">
                    <img
                        className="center-block phone-main"
                        src={require("../static/images/phone_main.png")}
                    />
                </div>
            </div>
        )
    }
}

class SignUpPanel extends React.Component{
    constructor (props) {
        super(props);
    }

    componentDidMount() {
        console.log(this.props.switchParentPanel)
    }
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
                <div className="col-lg-6 col-md-6 col-sm-6 visible-lg">
                    <h1> </h1>
                </div>
                <div className="signup-form-panel-2">
                    <div className="col-lg-4 col-md-4 col-sm-6 login-form-panel-two">
                        <div className="text-center signup-switch">
                            <h5>
                                Have an account?
                                <button
                                    type="button"
                                    onClick={this.props.switchParentPanel}
                                    className="btn btn-link signup-btn-switch">
                                    Login
                                </button>
                            </h5>
                        </div>
                    </div>
                </div>
                <AppIcons/>
            </div>
        )
    }
}

class SignUpForm extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            isValidEmail: false,
            isValidFirstName: false,
            isValidLastName: false,
            isValidUsername: false,
            isValidPassword: false,
            isValidDOB: false,
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
                let isValid = validateUsernameEmail(data, value, name);
                if(name === "email"){
                    this.setState({
                        isValidEmail: isValid,
                    })
                }

            }).catch(function (error) {
                console.log(error)
            });
        } else if(name === "first_name"){
            let isValid = validateNamePasswordDOB(value, 13, 2);
            this.setState({
                isValidFirstName: isValid,
            })
        } else if(name === "last_name"){
            debugger;
            const isValid = validateNamePasswordDOB(value, 14, 2);
            console.log(isValid)
            this.setState({
                isValidLastName: isValid,
            })
            debugger
        } else if(name === "password"){
            let isValid = validateNamePasswordDOB(value, 15, 5);
            this.setState({
                isValidPassword: isValid,
            })
        } else if(name === "date_of_birth"){
            let isValid = validateNamePasswordDOB(value, 16, 2);
            this.setState({
                isValidDOB: isValid,
            })
        }
    }

    handleSubmit(event){
        console.log(this.state.email);
        event.preventDefault();
    //    validate data
    //    fetch api here and send data
        if(
            !(this.state.isValidEmail &&
            this.state.isValidFirstName &&
            this.state.isValidLastName &&
            this.state.isValidUsername &&
            this.state.isValidPassword &&
            this.state.isValidDOB)
        ){
            alert('Please correct all errors..')
        }
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
                <div className="form-group signup-field">
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
                        className="form-control signup-username"
                        name="username"
                        type="text"
                        placeholder="Username"
                        onChange={this.handleInputChange}
                    /> <br/>
                </div>
                <div className="form-group signup-field">
                    <input
                        className="form-control signup-password"
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

export default SignUp;