import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { signup } from '../actions/userActions';
import PropTypes from 'prop-types';
import { reactAppConstants } from '../constants/constants';
import { routeConstants } from '../constants/routeConstants';
import { Container } from '@material-ui/core';
import Card from '@material-ui/core/Card';
import TextField from '@material-ui/core/TextField';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';

class Signup extends React.Component {

    state = {
        username: null,
        password1: null,
        password2: null,
        email: null,
        user_type: reactAppConstants.CUSTOMER,
        userTypeIndex:0
    }

    cardStyle = {
        marginTop: '15%',
        padding: '20px'
    }

    textieldStyle = {
        width: '100%'
    }

    handleChange = e => {
        let nam = e.target.name;
        let val = e.target.value;
        this.setState({ [nam]: val });
    }
    handleSubmit = e => {
        e.preventDefault();
        this.props.signup(this.state.username, this.state.email, this.state.password1, this.state.password2, this.state.user_type).then(() => {
            if (this.props.signupFailed) {
                toast.error('Sign Up Failed!');
            }
            else{
                this.props.history.push(routeConstants.LOGIN_ROUTE);
            }

        });
    }
    handleTabClick = userType => {
        let tabIndex;
        userType===reactAppConstants.CUSTOMER?(
            tabIndex = 0
        ):(
            tabIndex = 1
        );
        this.setState({ [reactAppConstants.USER_TYPE]: userType,userTypeIndex:tabIndex});

    }

    render() {
        let tabClassCustomer = ['nav-link'];
        let tabClassSaloon = ['nav-link'];
        let passwordCheck = this.state.password1 === this.state.password2;
        if (this.state.user_type === reactAppConstants.CUSTOMER) {
            tabClassCustomer.push('active');
        }
        else {
            tabClassSaloon.push('active');
        }
        return (
            <Container maxWidth="sm">
                <ToastContainer />
                <Card style={this.cardStyle}>
                    <Typography variant="h4">
                            Sign Up
                    </Typography>
                    <Tabs
                        value={this.state.userTypeIndex}
                        indicatorColor="primary"
                        textColor="primary"
                        variant="fullWidth"
                    >
                        <Tab label="Customer" onClick={()=>this.handleTabClick('customer')} />
                        <Tab label="Saloon" onClick={()=>this.handleTabClick('saloon')}/>
                    </Tabs>
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
                            id="outlined-email"
                            label="email"
                            required
                            name="email"
                            style={this.textieldStyle}
                            onChange={this.handleChange}
                            margin="normal"
                            variant="outlined"
                            type='email'
                        />
                        <TextField
                            id="outlined-password2"
                            label="Confrim Password"
                            required
                            name="password2"
                            style={this.textieldStyle}
                            onChange={this.handleChange}
                            margin="normal"
                            variant="outlined"
                            type='password'
                        />
                        <TextField
                            id="outlined-password1"
                            label="Password"
                            required
                            name="password1"
                            style={this.textieldStyle}
                            onChange={this.handleChange}
                            margin="normal"
                            variant="outlined"
                            type='password'
                        />
                        {!passwordCheck && <Typography variant="h6" style={{color:'red'}}>
                            Password does not match
                        </Typography>}
                        {passwordCheck ? (
                            <Button type="submit" variant="contained" color="primary">
                            Sign up
                            </Button>
                        ) : (
                            <Button type="submit" disabled variant="contained" color="primary">
                            Sign up
                            </Button>
                        )}
                        <br /><br />
                        <Typography variant="h6">
                            <Link to={routeConstants.LOGIN_ROUTE} style={{ textDecoration: 'none'}}>Login</Link>
                        </Typography>
                    </form>
                </Card>
            </Container>
        );
    }

}

Signup.propTypes = {
    signupFailed: PropTypes.bool.isRequired,
    signup: PropTypes.func.isRequired,
    history: PropTypes.object.isRequired
};

const mapStateToPropos = state =>
    (
        {
            signupFailed: state.user.signupFailed
        }
    );


const mapDispatchToProps = dispatch =>
    (
        {
            signup: (username, email, password1, password2, user_type) => dispatch(signup(username, email, password1, password2, user_type))
        }
    );

export default connect(mapStateToPropos, mapDispatchToProps)(Signup);