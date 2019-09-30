import React, { Component } from 'react';
import { compose } from 'redux';
import { connect } from 'react-redux';
import localStorage from 'local-storage';
import PropTypes from 'prop-types';
import { saloonProfile, updateSaloonProfile } from '../actions/saloonActions';
import { customerProfile, updateCustomerProfile } from '../actions/customerActions';
import { userValueUpdate } from '../actions/userActions';
import IsAuthenticated from '../hoc/isAuthenticated';
import { reactAppConstants } from '../constants/constants';
import { Container } from '@material-ui/core';
import Card from '@material-ui/core/Card';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import { Field, reduxForm } from 'redux-form';
import {renderField,validate} from './RenderField';
import withStyles from '@material-ui/styles/withStyles';
import { appStyles } from '../styles/appStyles';

class Profile extends Component {

    componentDidMount() {
        const userType = localStorage.get(reactAppConstants.USER_TYPE);
        userType === reactAppConstants.CUSTOMER ? (
            this.props.customerProfile()
        ) : (
            this.props.saloonProfile()
        );
    }

    formSubmit = values => {
        const userType = localStorage.get(reactAppConstants.USER_TYPE);
        if (userType === reactAppConstants.CUSTOMER) {
            this.props.updateCustomerProfile(values).then(() => {
                this.props.updateStatus && toast.success('Profile Updated');
            });
        } else if (userType === reactAppConstants.SALOON) {
            this.props.updateSaloonProfile(values).then(() => {
                this.props.updateStatus && toast.success('Profile Updated');
            });
        }

    }

    render() {
        const { classes } = this.props;
        const { initialValues } = this.props;
        const { handleSubmit} = this.props;
        const { invalid } = this.props;
        const userType = localStorage.get(reactAppConstants.USER_TYPE);
        const userProfile = (initialValues && <Container maxWidth="sm">
            <ToastContainer />
            <Card className={classes.authCard}>
                <Typography variant="h4">
                        Profile
                </Typography>
                <form onSubmit={handleSubmit(this.formSubmit)}>
                    <Field
                        id="outlined-email"
                        label="Email"
                        name="email"
                        className={classes.textFieldStyle}
                        required
                        component={renderField}
                        type='email'
                    />
                    <Field
                        id="outlined-username"
                        label="Username"
                        name="username"
                        className={classes.textFieldStyle}
                        required
                        component={renderField}
                        type='text'
                    />
                    <Field
                        id="outlined-first_name"
                        label="First Name"
                        name="first_name"
                        className={classes.textFieldStyle}
                        required
                        component={renderField}
                        type='text'
                    />
                    <Field
                        id="outlined-last_name"
                        label="Last Name"
                        name="last_name"
                        className={classes.textFieldStyle}
                        required
                        component={renderField}
                        type='text'
                    />
                    <Field
                        id="outlined-phone_no"
                        label="Phone No"
                        name="phone_no"
                        className={classes.textFieldStyle}
                        required
                        component={renderField}
                        type='number'
                    />
                    {userType === reactAppConstants.SALOON &&
                        <React.Fragment>
                            <Field
                                id="outlined-shop_name"
                                label="Shop Name"
                                name="shop_name"
                                className={classes.textFieldStyle}
                                required
                                component={renderField}
                                onChange={this.handleChange}
                                margin="normal"
                                variant="outlined"
                                type='text'
                            />
                            <Field
                                id="outlined-address"
                                label="Address"
                                name="address"
                                className={classes.textFieldStyle}
                                required
                                component={renderField}
                                onChange={this.handleChange}
                                margin="normal"
                                variant="outlined"
                                type='textarea'
                            />
                        </React.Fragment>}
                    <Button type="submit" disabled={invalid} variant="contained" color="primary">Submit</Button>
                </form>
            </Card>
        </Container>);
        return (
            <React.Fragment>
                {userProfile}
            </React.Fragment>
        );
    }
}

Profile.propTypes = {
    initialValues: PropTypes.object.isRequired,
    updateStatus:PropTypes.bool.isRequired,
    customerProfile: PropTypes.func.isRequired,
    updateCustomerProfile: PropTypes.func.isRequired,
    saloonProfile:PropTypes.func.isRequired,
    updateSaloonProfile: PropTypes.func.isRequired,
    userValueUpdate: PropTypes.func.isRequired,
    handleSubmit:PropTypes.func.isRequired,
    invalid:PropTypes.bool.isRequired,
    classes:PropTypes.object.isRequired
};

const mapStateToProps = state => ({
    initialValues: state.user.user,
    updateStatus: state.user.updateStatus
});

const mapDispatchToProps = dispatch => ({
    customerProfile: () => dispatch(customerProfile()),
    updateCustomerProfile: (data) => dispatch(updateCustomerProfile(data)),
    saloonProfile: () => dispatch(saloonProfile()),
    updateSaloonProfile: (data) => dispatch(updateSaloonProfile(data)),
    userValueUpdate: (key, val) => dispatch(userValueUpdate(key, val))
});
    
export default compose(
    connect(mapStateToProps, mapDispatchToProps),
    IsAuthenticated,
    reduxForm({
        form: 'signupForm',
        validate:validate,
        enableReinitialize: true
    }),
    withStyles(appStyles)
)(Profile);
