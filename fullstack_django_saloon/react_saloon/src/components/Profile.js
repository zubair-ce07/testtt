import React, { Component } from 'react';
import { compose } from 'redux';
import { connect } from 'react-redux';
import ls from 'local-storage';
import PropTypes from 'prop-types';

import { saloonProfile, updateSaloonProfile } from '../actions/saloonActions';
import { customerProfile, updateCustomerProfile } from '../actions/customerActions';
import { userValueUpdate } from '../actions/userActions';
import IsAuthenticated from '../hoc/isAuthenticated';
import { reactAppConstants } from '../constants/constants';

import { Container } from '@material-ui/core';
import Card from '@material-ui/core/Card';
import TextField from '@material-ui/core/TextField';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

class Profile extends Component {
    cardStyle = {
        marginTop: '15%',
        padding: '20px'
    }

    textieldStyle = {
        width: '100%'
    }

    componentDidMount() {
        const userType = ls.get(reactAppConstants.USER_TYPE);
        userType === reactAppConstants.CUSTOMER ? (
            this.props.customerProfile()
        ) : (
            this.props.saloonProfile()
        );
    }

    handleChange = e => {
        let key = e.target.name;
        let val = e.target.value;
        this.props.userValueUpdate(key, val);
    }
    handleSubmit = e => {
        e.preventDefault();
        const userType = ls.get(reactAppConstants.USER_TYPE);
        if (userType === reactAppConstants.CUSTOMER) {
            this.props.updateCustomerProfile(this.props.user).then(() => {
                this.props.updateStatus && toast.success('Profile Updated');
            });
        } else if (userType === reactAppConstants.SALOON) {
            this.props.updateSaloonProfile(this.props.user).then(() => {
                this.props.updateStatus && toast.success('Profile Updated');
            });
        }

    }

    render() {
        const { user } = this.props;
        const userType = ls.get(reactAppConstants.USER_TYPE);
        const userProfile = (user && <Container maxWidth="sm" style={{ width: '100%' }}>
            <ToastContainer />
            <Card style={this.cardStyle}>
                <Typography variant="h4">
                        Profile
                </Typography>
                <form onSubmit={this.handleSubmit}>
                    <TextField
                        id="outlined-email"
                        label="Email"
                        name="email"
                        value={user.email || ''}
                        style={this.textieldStyle}
                        required
                        onChange={this.handleChange}
                        margin="normal"
                        variant="outlined"
                        type='email'
                    />
                    <TextField
                        id="outlined-username"
                        label="Username"
                        name="username"
                        value={user.username || ''}
                        style={this.textieldStyle}
                        required
                        onChange={this.handleChange}
                        margin="normal"
                        variant="outlined"
                        type='text'
                    />
                    <TextField
                        id="outlined-first_name"
                        label="First Name"
                        name="first_name"
                        value={user.first_name || ''}
                        style={this.textieldStyle}
                        required
                        onChange={this.handleChange}
                        margin="normal"
                        variant="outlined"
                        type='text'
                    />
                    <TextField
                        id="outlined-last_name"
                        label="Last Name"
                        name="last_name"
                        value={user.last_name || ''}
                        style={this.textieldStyle}
                        required
                        onChange={this.handleChange}
                        margin="normal"
                        variant="outlined"
                        type='text'
                    />
                    <TextField
                        id="outlined-phone_no"
                        label="Phone No"
                        name="phone_no"
                        value={user.phone_no || ''}
                        style={this.textieldStyle}
                        required
                        onChange={this.handleChange}
                        margin="normal"
                        variant="outlined"
                        type='number'
                    />
                    {userType === reactAppConstants.SALOON &&
                        <React.Fragment>
                            <TextField
                                id="outlined-shop_name"
                                label="Shop Name"
                                name="shop_name"
                                value={user.shop_name || ''}
                                style={this.textieldStyle}
                                required
                                onChange={this.handleChange}
                                margin="normal"
                                variant="outlined"
                                type='text'
                            />
                            <TextField
                                id="outlined-address"
                                label="Address"
                                name="address"
                                value={user.address || ''}
                                style={this.textieldStyle}
                                required
                                onChange={this.handleChange}
                                margin="normal"
                                variant="outlined"
                                type='textarea'
                            />
                        </React.Fragment>}
                    <Button type="submit" variant="contained" color="primary">Submit</Button>
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
    user: PropTypes.object.isRequired,
    updateStatus:PropTypes.bool.isRequired,
    customerProfile: PropTypes.func.isRequired,
    updateCustomerProfile: PropTypes.func.isRequired,
    saloonProfile:PropTypes.func.isRequired,
    updateSaloonProfile: PropTypes.func.isRequired,
    userValueUpdate: PropTypes.func.isRequired
};

const mapStateToProps = state =>
    (
        {
            user: state.user.user,
            updateStatus: state.user.updateStatus
        }
    );

const mapDispatchToProps = dispatch => 
    (
        {
            customerProfile: () => dispatch(customerProfile()),
            updateCustomerProfile: (data) => dispatch(updateCustomerProfile(data)),
            saloonProfile: () => dispatch(saloonProfile()),
            updateSaloonProfile: (data) => dispatch(updateSaloonProfile(data)),
            userValueUpdate: (key, val) => dispatch(userValueUpdate(key, val))
        }   
    );
    
export default compose(
    IsAuthenticated,
    connect(mapStateToProps, mapDispatchToProps)
)(Profile);
