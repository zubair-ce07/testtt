import React from 'react';
import { connect } from 'react-redux';
import { compose } from 'redux';
import { Link } from 'react-router-dom';
import { login } from '../actions/userActions';
import PropTypes from 'prop-types';
import { routeConstants } from '../constants/routeConstants';
import Container from '@material-ui/core/Container';
import Card from '@material-ui/core/Card';
import { ToastContainer,toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import { Field, reduxForm } from 'redux-form';
import {renderField,validate} from './RenderField';




class Login extends React.Component {
    cardStyle = {
        marginTop: '15%',
        padding: '20px'
    }

    textFieldStyle = {
        width: '100%'
    }
    
    formSubmit = values => {
        this.props.login(values.username, values.password).then(() => {
            if (!this.props.LoginFailed) {
                this.props.history.push(routeConstants.LIST_SALOONS_ROUTE);
            }
            else{
                toast.error('Login Failed!');
            }
        });
    };

    render() {
        const { handleSubmit} = this.props;
        const { invalid } = this.props;

        return (
            <Container maxWidth="sm">
                <ToastContainer />
                <Card style={this.cardStyle}>
                    <Typography variant="h4">
                            Login
                    </Typography>
                    <form onSubmit={handleSubmit(this.formSubmit)}>
                        <Field
                            id="outlined-username"
                            label="Username"
                            required
                            name="username"
                            component={renderField}
                            style={this.textFieldStyle}
                            type='text'
                        />
                        <Field
                            id="outlined-password"
                            label="Password"
                            required
                            name="password"
                            component={renderField}
                            style={this.textFieldStyle}
                            type='password'
                        />
                        <Button type="submit" disabled={invalid} variant="contained" color="primary">
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
    history:PropTypes.object.isRequired,
    handleSubmit:PropTypes.func.isRequired,
    invalid:PropTypes.bool.isRequired

};

const mapStateToProps = state => ({
    LoginFailed: state.user.LoginFailed
});


const mapDispatchToProps = dispatch => ({
    login: (username, password) => dispatch(login(username, password))
});

export default compose(
    connect(mapStateToProps, mapDispatchToProps),
    reduxForm({
        form: 'loginForm',
        validate:validate,
    })
)(Login);
