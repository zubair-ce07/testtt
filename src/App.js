import React from 'react';
import './App.css';
import AppSidebar from './SharedComponents/AppSidebar/AppSidebar';
import {createMuiTheme} from "@material-ui/core";
import {ThemeProvider} from '@material-ui/styles';
import NewsFeed from "./PostComponents/NewsFeed";
import profile from "./UserComponents/Profile/Profile";
import {BrowserRouter, Route} from "react-router-dom";

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            user: null,
            token: null
        }
    }

    theme = createMuiTheme({
        palette: {
            primary: {main: '#4AA8E0'}
        }
    });

    handleUser = (user, token) => {
        this.setState({
            user: user,
            token: token
        });

        localStorage.setItem('user', user);
        localStorage.setItem('token', token);
    };

    componentDidMount() {
        let user = localStorage.getItem('user');
        let token = localStorage.getItem('token');
        if (user && token) {
            this.handleUser(user, token)
        }
    }

    render() {
        return (
            <ThemeProvider theme={this.theme}>
                <BrowserRouter>
                    <div className="App">
                        <AppSidebar user={this.state.user} handleUser={this.handleUser}/>
                    </div>
                    <div style={{marginLeft: 240}}>
                        <switch>
                            <Route path="/home" component={NewsFeed}/>
                            <Route path="/profile" component={profile}/>
                        </switch>
                    </div>
                </BrowserRouter>
            </ThemeProvider>
        );
    }
}

export default App;
