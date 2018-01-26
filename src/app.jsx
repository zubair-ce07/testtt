import React from "react";
import "./app.css";
import Login from "./login";
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";
import AppBar from "material-ui/AppBar";
import {Tab, Tabs} from "material-ui/Tabs";
import SignUp from "./signup";
import createBrowserHistory from "history/createBrowserHistory";
import {Router, Route} from "react-router";
import {connect} from 'react-redux'


const newHistory = createBrowserHistory();

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
                <AppBar title="React Practice" style={styles.appBar}
                        iconClassNameRight="muidocs-icon-navigation-expand-more">
                    <Tabs label="Home" style={styles.tabs}>
                        <Tab label="Home"/>
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

    render() {
        let login = "";
        let signup = "";

        if (this.props.showLogin) {
            login = (
                <Login submit='#'/>
            )
        }
        if (this.props.showSignUp) {
            signup = (
                <SignUp/>
            )
        }
        return (
            <div>
                <NavBar onClickLogin={this.props.loginShow} onClickSignUp={this.props.signUpShow}/>
                {login}
                {signup}
            </div>
        )
    }
}

const mapStateToProp = (state) => {
    return {
        toggle: state.reducer,
    }
};

const mapDispatchToProps = (dispatch) => {
  return{
      loginShow: () => {
          dispatch({
              type: "SHOW_LOGIN"
          })
      },
      signUpShow: () => {
          dispatch({
              type: "SHOW_SIGN_UP"
          })
      }
  }
};

class Root extends React.Component {
    render() {
        return (
            <Router history={newHistory}>
                <div>
                    <Route exact path="/" render={
                        ()=><UI showLogin={this.props.toggle.showLogin}
                                showSignUp={this.props.toggle.showSignUp}
                                loginShow={this.props.loginShow}
                                signUpShow={this.props.signUpShow}
                        />
                    }/>
                    <Route path="/login" component={Login}/>
                    <Route path="/signup" component={SignUp}/>
                </div>
            </Router>
        )
    }
}


export default connect(mapStateToProp, mapDispatchToProps)(Root);