import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";
import RaisedButton from "material-ui/RaisedButton";
import TextField from "material-ui/TextField";
import React from "react";

class SignUp extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: '',
            repassword: '',
            fullname: '',
        }
    }
    handleClick(event){
        alert('User Name : '+this.state.username);
        alert('Password : '+this.state.password);
    }
    render() {
        return (
            <div>
                <MuiThemeProvider>
                    <div>
                        <TextField
                            hintText="Enter Username"
                            floatingLabelText="Username"
                            onChange={(event, newValue) => this.setState({username: newValue})}
                        />
                        <br/>
                        <TextField
                            type="password"
                            hintText="Enter your Password"
                            floatingLabelText="Password"
                            onChange={(event, newValue) => this.setState({password: newValue})}
                        />
                        <br/>
                        <TextField
                            type="password"
                            hintText="Confirm your Password"
                            floatingLabelText="Confirm Password"
                            onChange={(event, newValue) => this.setState({repassword: newValue})}
                        />
                        <br/>
                        <TextField
                            type="text"
                            hintText="Full Name"
                            floatingLabelText="Your Full Name"
                            onChange={(event, newValue) => this.setState({fullname: newValue})}
                        />
                        <br/>
                        <RaisedButton label="Register" primary={true} style={style}
                                      onClick={(event) => this.handleClick(event)}/>
                    </div>
                </MuiThemeProvider>
            </div>
        );
    }
}
const style = {
    margin: 15,
};
export default SignUp;