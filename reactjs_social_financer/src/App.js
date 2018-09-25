import React, { Component } from 'react';
import './App.css';
import MyRouter from './modules/Router'
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import blue from '@material-ui/core/colors/blue';
import green from '@material-ui/core/colors/green';
import red from '@material-ui/core/colors/red';
import CssBaseline from '@material-ui/core/CssBaseline';

const theme = createMuiTheme({
  palette: {
    primary: blue,
    secondary: green,
    error: red,
  },
});

class App extends Component {
  render() {
    return (
    <MuiThemeProvider theme={theme}>
      <CssBaseline />
      <MyRouter />
    </MuiThemeProvider>
  );
  }
}



export default App;
