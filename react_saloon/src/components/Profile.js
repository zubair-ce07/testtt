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

class Profile extends Component {

    state = {
        updateSuccess:false
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
        this.setState({updateSuccess:false});
        e.preventDefault();
        const userType = ls.get(reactAppConstants.USER_TYPE);
        if (userType === reactAppConstants.CUSTOMER) {
            this.props.updateCustomerProfile(this.props.user).then(() => {
                this.props.updateStatus && this.setState({updateSuccess:true});
            });
        } else if (userType === reactAppConstants.SALOON) {
            this.props.updateSaloonProfile(this.props.user).then(() => {
                this.props.updateStatus && this.setState({updateSuccess:true});
            });
        }

    }

    render() {
        const { user } = this.props;
        const userType = ls.get(reactAppConstants.USER_TYPE);
        const userProfile = (user && <div style={{ width: '100%' }}>
            <center><h2>Profile</h2></center>
            <form onSubmit={this.handleSubmit}>
                <div className="fouser_actionsm-group">
                    <label htmlFor="exampleInputEmail1">Email address</label>
                    <input required type="email" name='email' onChange={this.handleChange} value={user.email || ''} className="form-control" id="exampleInputEmail1" placeholder="Enter email" />
                </div>
                <div className="form-group">
                    <label htmlFor="username">Username</label>
                    <input required type="text" name='username' onChange={this.handleChange} value={user.username || ''} className="form-control" id="usename" placeholder="Enter Username" />
                </div>
                <div className="form-group">
                    <label htmlFor="first_name">First Name</label>
                    <input required type="text" name='first_name' onChange={this.handleChange} value={user.first_name || ''} className="form-control" id="first_name" placeholder="Enter First Name" />
                </div>
                <div className="form-group">
                    <label htmlFor="last_name">Last Name</label>
                    <input required type="text" name='last_name' onChange={this.handleChange} value={user.last_name || ''} className="form-control" id="last_name" placeholder="Enter Last Name" />
                </div>
                <div className="form-group">
                    <label htmlFor="phone_no">Phone No</label>
                    <input required type="number" name='phone_no' onChange={this.handleChange} value={user.phone_no || ''} className="form-control" id="phone_no" placeholder="Enter Phone No" />
                </div>
                {userType === reactAppConstants.SALOON &&
                    <React.Fragment>
                        <div className="form-group">
                            <label htmlFor="shop_name">Shop Name</label>
                            <input required type="text" name='shop_name' onChange={this.handleChange} value={user.shop_name || ''} className="form-control" id="shop_name" placeholder="Enter Shop Name" />
                        </div>
                        <div className="form-group">
                            <label htmlFor="shop_name">Address</label>
                            <textarea required type="text" name='address' onChange={this.handleChange} value={user.address || ''} className="form-control" id="address" placeholder="Enter Shop Address"></textarea>
                        </div>
                    </React.Fragment>}
                <button type="submit" className="btn btn-primary">Submit</button>
            </form>
        </div>);
        const successMessage = this.state.updateSuccess &&
            <div className="alert alert-success" role="alert" >
                Profile Updated!</div>;
        // const error_message = this.state.update_error &&
        // <div className="alert alert-error" role="alert" >
        //     Error Updating Profile!</div>
        return (
            <div className='container' >
                {successMessage}
                {userProfile}
            </div >
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
