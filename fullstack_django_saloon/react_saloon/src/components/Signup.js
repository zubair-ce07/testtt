import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { compose } from 'redux';
import { signup } from '../actions/userActions';
import PropTypes from 'prop-types';
import { reactAppConstants } from '../constants/constants';
import { routeConstants } from '../constants/routeConstants';
import { Container } from '@material-ui/core';
import Card from '@material-ui/core/Card';
import { ToastContainer,toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import { Field, reduxForm } from 'redux-form';
import {renderField,validate} from './RenderField';

class Signup extends React.Component {

    state = {
        user_type: reactAppConstants.CUSTOMER,
        userTypeIndex:0
    }

    cardStyle = {
        marginTop: '15%',
        padding: '20px'
    }

    textFieldStyle = {
        width: '100%'
    }

    formSubmit = values => {
        this.props.signup(values.username, values.email, values.password1, values.password2, this.state.user_type).then(() => {
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
        const { handleSubmit} = this.props;
        const { invalid } = this.props;
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
                    <form onSubmit={handleSubmit(this.formSubmit)}>
                        <Field
                            id="outlined-username"
                            label="Username"
                            name="username"
                            style={this.textFieldStyle}
                            component={renderField}
                            required
                            type='text'
                        />
                        <Field
                            id="outlined-email"
                            label="email"
                            required
                            name="email"
                            style={this.textFieldStyle}
                            component={renderField}
                            type='email'
                        />
                        <Field
                            id="outlined-password1"
                            label="Password"
                            required
                            name="password1"
                            style={this.textFieldStyle}
                            component={renderField}
                            type='password'
                        />
                        <Field
                            id="outlined-password2"
                            label="Confrim Password"
                            required
                            name="password2"
                            style={this.textFieldStyle}
                            component={renderField}
                            type='password'
                        />
                        <input hidden type='text' value={this.state.user_type} name='user_type' readOnly/>
                        <Button type="submit" disabled={invalid} variant="contained" color="primary">
                        Sign up
                        </Button>
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
    history: PropTypes.object.isRequired,
    handleSubmit:PropTypes.func.isRequired,
    invalid:PropTypes.bool.isRequired
};

const mapStateToProps = state =>
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

export default compose(
    connect(mapStateToProps, mapDispatchToProps),
    reduxForm({
        form: 'signupForm',
        validate:validate,
    })
)(Signup);