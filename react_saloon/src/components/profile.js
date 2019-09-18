import React, { Component } from 'react';
import { compose } from 'redux';
import { connect } from 'react-redux';
import ls from 'local-storage';
import PropTypes from 'prop-types';

import { saloon_profile, update_saloon_profile } from '../actions/saloon_action';
import { customer_profile, update_customer_profile } from '../actions/customer_actions';
import { user_value_update } from '../actions/user_actions';
import isAuthneticated from '../hoc/isAuthenticated';
class profile extends Component {

    componentDidMount() {
        const user_type = ls.get('user_type');
        user_type === 'customer' ? (
            this.props.customer_profile()
        ) : (
            this.props.saloon_profile()
        );
    }

    handleChange = (e) => {
        let key = e.target.name;
        let val = e.target.value;
        this.props.user_value_update(key, val);
    }
    handleSubmit = (e) => {
        e.preventDefault();
        const user_type = ls.get('user_type');
        if (user_type === 'customer') {
            this.props.update_customer_profile(this.props.user);
        } else if (user_type === 'saloon') {
            this.props.update_saloon_profile(this.props.user);
        }

    }

    render() {
        const { user } = this.props;
        const user_type = ls.get('user_type');
        const user_profile = (user && <div style={{ width: '100%' }}>
            <center><h2>Profile</h2></center>
            <form onSubmit={this.handleSubmit}>
                <div className="form-group">
                    <label htmlFor="exampleInputEmail1">Email address</label>
                    <input required type="email" name='email' onChange={this.handleChange} value={user.email} className="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email" />
                </div>
                <div className="form-group">
                    <label htmlFor="username">Username</label>
                    <input required type="text" name='username' onChange={this.handleChange} value={user.username} className="form-control" id="usename" placeholder="Enter Username" />
                </div>
                <div className="form-group">
                    <label htmlFor="first_name">First Name</label>
                    <input required type="text" name='first_name' onChange={this.handleChange} value={user.first_name} className="form-control" id="first_name" placeholder="Enter First Name" />
                </div>
                <div className="form-group">
                    <label htmlFor="last_name">Last Name</label>
                    <input required type="text" name='last_name' onChange={this.handleChange} value={user.last_name} className="form-control" id="last_name" placeholder="Enter Last Name" />
                </div>
                <div className="form-group">
                    <label htmlFor="phone_no">Phone No</label>
                    <input required type="number" name='phone_no' onChange={this.handleChange} value={user.phone_no} className="form-control" id="phone_no" placeholder="Enter Phone No" />
                </div>
                {user_type === 'saloon' &&
                    <React.Fragment>
                        <div className="form-group">
                            <label htmlFor="shop_name">Shop Name</label>
                            <input required type="text" name='shop_name' onChange={this.handleChange} value={user.shop_name} className="form-control" id="shop_name" placeholder="Enter Shop Name" />
                        </div>
                        <div className="form-group">
                            <label htmlFor="shop_name">Address</label>
                            <textarea required type="text" name='address' onChange={this.handleChange} value={user.address} className="form-control" id="address" placeholder="Enter Shop Address"></textarea>
                        </div>
                    </React.Fragment>}
                <button type="submit" className="btn btn-primary">Submit</button>
            </form>
        </div>);
        // const sucess_message = this.props.update_status &&
        //     <div className="alert alert-success" role="alert" >
        //         Profile Updated!</div>
        return (
            <div className='container' >
                {/* {sucess_message} */}
                {user_profile}
            </div >
        );
    }
}

profile.propTypes = {
    user: PropTypes.object.isRequired,
    update_status:PropTypes.bool.isRequired,
    customer_profile: PropTypes.func.isRequired,
    update_customer_profile: PropTypes.func.isRequired,
    saloon_profile: () => PropTypes.func.isRequired,
    update_saloon_profile: PropTypes.func.isRequired,
    user_value_update: PropTypes.func.isRequired
};

const mapStateToProps = (state) => {
    return {
        user: state.user.user,
        update_status: state.user.update_status
    };
};

const mapDispatchToProps = dispatch => {
    return {
        customer_profile: () => dispatch(customer_profile()),
        update_customer_profile: (data) => dispatch(update_customer_profile(data)),
        saloon_profile: () => dispatch(saloon_profile()),
        update_saloon_profile: (data) => dispatch(update_saloon_profile(data)),
        user_value_update: (key, val) => dispatch(user_value_update(key, val))
    };
};
export default compose(
    isAuthneticated,
    connect(mapStateToProps, mapDispatchToProps)
)(profile);
