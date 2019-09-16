import React, { Component } from 'react'
import { connect } from 'react-redux'
import ls from 'local-storage'

import { customer_profile, saloon_profile } from '../actions/saloon_action'

export class profile extends Component {

    componentDidMount() {
        const user_type = ls.get('user_type')
        user_type === 'customer' ? (
            this.props.customer_profile()
        ) : (
                this.props.saloon_profile()
            )
    }

    handleChange = (e) => {
        let nam = e.target.name;
        let val = e.target.value;
        this.setState({ [nam]: val });
    }
    handleSubmit = (e) => {
        e.preventDefault();

    }

    render() {
        const { user } = this.props
        console.log(user)
        const user_type = ls.get('user_type')
        const user_profile = (user && <div style={{ width: '100%' }}>
            <center><h2>Profile</h2></center>
            <form onSubmit={this.handleSubmit}>
                <div className="form-group">
                    <label htmlFor="exampleInputEmail1">Email address</label>
                    <input type="email" onChange={this.handleChange} value={user.user.email} className="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email" />
                </div>
                <div className="form-group">
                    <label htmlFor="username">Username</label>
                    <input type="text" onChange={this.handleChange} value={user.user.username} className="form-control" id="usename" placeholder="Enter Username" />
                </div>
                <div className="form-group">
                    <label htmlFor="first_name">First Name</label>
                    <input type="text" onChange={this.handleChange} value={user.user.first_name} className="form-control" id="first_name" placeholder="Enter First Name" />
                </div>
                <div className="form-group">
                    <label htmlFor="last_name">Last Name</label>
                    <input type="text" onChange={this.handleChange} value={user.user.last_name} className="form-control" id="last_name" placeholder="Enter Last Name" />
                </div>
                <div className="form-group">
                    <label htmlFor="phone_no">Phone No</label>
                    <input type="number" onChange={this.handleChange} value={user.phone_no} className="form-control" id="phone_no" placeholder="Enter Phone No" />
                </div>
                {user_type === 'saloon' &&
                    <React.Fragment>
                        <div className="form-group">
                            <label htmlFor="shop_name">Shop Name</label>
                            <input type="text" onChange={this.handleChange} value={user.shop_name} className="form-control" id="shop_name" placeholder="Enter Shop Name" />
                        </div>
                        <div className="form-group">
                            <label htmlFor="shop_name">Address</label>
                            <textarea type="text" onChange={this.handleChange} value={user.address} className="form-control" id="address" placeholder="Enter Shop Address"></textarea>
                        </div>
                    </React.Fragment>}
                <button type="submit" className="btn btn-primary">Submit</button>
            </form>
        </div>)
        return (
            <div className='container' >
                {user_profile}
            </div >
        )
    }
}

const mapStateToProps = (state) => {
    return {
        user: state.user
    }
}

const mapDispatchToProps = dispatch => {
    return {
        customer_profile: () => dispatch(customer_profile()),
        saloon_profile: () => dispatch(saloon_profile())
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(profile)
