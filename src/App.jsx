import React from 'react';
import './app.css'
import Login from './login'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import AppBar from 'material-ui/AppBar'
import {Tab, Tabs} from 'material-ui/Tabs'
import SignUp from './signup'


const styles = {
   appBar: {
     flexWrap: 'wrap',
   },
   tabs: {
     width: '100%',
   },
 };

class NavBar extends React.Component {
    render() {
        return (
            <MuiThemeProvider>
                <AppBar title="React Practice" style={styles.appBar} iconClassNameRight="muidocs-icon-navigation-expand-more" >
                    <Tabs label="Home" style={styles.tabs}>
                        <Tab label="Home" />
                        <Tab onActive={this.props.onClickLogin} label="Login"/>
                        <Tab onActive={this.props.onClickSignUp} label="Sign Up"/>
                        <Tab label="About Us"/>
                        <Tab label="Careers"/>
                        <Tab label="Contact"/>
                    </Tabs>
                </AppBar>
            </MuiThemeProvider>
        )
    }
}

class UI extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            showLogin: true,
            showSignUp: false,
        };
        this.loginShow = this.loginShow.bind(this);
        this.SignUpShow = this.SignUpShow.bind(this);
    }

    loginShow() {
        this.setState({showLogin: true, showSignUp: false});
    }

    SignUpShow() {
        this.setState({showSignUp: true, showLogin: false});
    }

    render() {
        let login = "";
        let signup = "";

        if (this.state.showLogin) {
            login = (
                <Login submit='#'/>
            )
        }
        if (this.state.showSignUp) {
            signup = (
                <SignUp/>
            )
        }
        return (
            <div>
                <NavBar onClickLogin={this.loginShow} onClickSignUp={this.SignUpShow}/>
                {login}
                {signup}
            </div>
        )
    }
}


export default UI;
