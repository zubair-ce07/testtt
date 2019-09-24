import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { login } from '../actions/userActions';
import PropTypes from 'prop-types';
import { routeConstants } from '../constants/routeConstants';


class Login extends React.Component {
    cardStyle = {
        marginTop: '15%'
    }
    state = {
        username: null,
        password: null
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
        });
    };

    render() {


        return (
            <div className='container'>
                {this.props.LoginFailed &&
                    <div className="alert alert-danger" role="alert" >
                        Login Failed!</div>}
                <div className="card" style={this.cardStyle}>
                    <div className="card-body">
                        <center><h2>Login</h2></center>
                        <form onSubmit={this.handleSubmit}>
                            <div className="form-group">
                                <label htmlFor="exampleInputEmail1">Username</label>
                                <input name='username' required type="text" onChange={this.handleChange} className="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email" />
                            </div>
                            <div className="form-group">
                                <label htmlFor="exampleInputPassword1">Password</label>
                                <input name='password' required type="password" onChange={this.handleChange} className="form-control" id="exampleInputPassword1" placeholder="Password" />
                            </div>
                            <button type="submit" className="btn btn-primary">Login</button>
                            <br /><br />
                            <Link to={routeConstants.SIGNUP_ROUTE}>Signup</Link>
                        </form>
                    </div>
                </div>
            </div>
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
