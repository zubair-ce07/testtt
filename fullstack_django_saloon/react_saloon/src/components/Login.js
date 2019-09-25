import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { login } from '../actions/userActions';
import PropTypes from 'prop-types';
import { routeConstants } from '../constants/routeConstants';
import { Container } from '@material-ui/core';
import Card from '@material-ui/core/Card';
import TextField from '@material-ui/core/TextField';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';




class Login extends React.Component {
    cardStyle = {
        marginTop: '15%',
        padding: '20px'
    }
    state = {
        username: null,
        password: null
    }

    textieldStyle = {
        width: '100%'
    }
      

    handleChange = (e) => {
        let nam = e.target.name;
        let val = e.target.value;
        this.setState({ [nam]: val });
    }
    handleSubmit = (e) => {
        e.preventDefault();
        this.props.login(this.state.username, this.state.password).then(() => {
            if (!this.props.LoginFailed) {
                this.props.history.push(routeConstants.LIST_SALOONS_ROUTE);
            }
            else{
                toast.error('Login Failed!');
            }
        });
    };

    render() {


        return (
            <Container maxWidth="sm">
                <ToastContainer />
                <Card style={this.cardStyle}>
                    <Typography variant="h4">
                            Login
                    </Typography>
                    <form onSubmit={this.handleSubmit}>
                        <TextField
                            id="outlined-username"
                            label="Username"
                            name="username"
                            style={this.textieldStyle}
                            required
                            onChange={this.handleChange}
                            margin="normal"
                            variant="outlined"
                            type='text'
                        />
                        <TextField
                            id="outlined-password"
                            label="Password"
                            required
                            name="password"
                            style={this.textieldStyle}
                            onChange={this.handleChange}
                            margin="normal"
                            variant="outlined"
                            type='password'
                        />
                        <Button type="submit" variant="contained" color="primary">
                            Login
                        </Button>
                        <br /><br />
                        <Typography variant="h6">
                            <Link to={routeConstants.SIGNUP_ROUTE} style={{ textDecoration: 'none'}}>Signup</Link>
                        </Typography>
                    </form>
                </Card>
            </Container>
        );
    }
}

Login.propTypes = {
    LoginFailed: PropTypes.bool.isRequired,
    login: PropTypes.func.isRequired,
    history:PropTypes.object.isRequired

};

const mapStateToPropos = state => 
    (
        {
            LoginFailed: state.user.LoginFailed
        }
    );


const mapDispatchToProps = dispatch =>
    (
        {
            login: (username, password) => dispatch(login(username, password))
        }
    );

export default connect(mapStateToPropos, mapDispatchToProps)(Login);
