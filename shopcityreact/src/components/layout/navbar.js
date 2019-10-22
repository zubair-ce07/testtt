import React from 'react';
import { Link} from 'react-router-dom';
import { connect } from 'react-redux';


const SignedInLinks = () => {
    return (
        <ul className="right">
            <li><Link to="#">View Cart</Link></li>
            <li><Link to="/register">Register</Link></li>
            <li><Link to="/login">Login</Link></li>
        </ul>
    )
};

const SignedOutLinks = () => {
    return (
        <ul className="right">
            <li><Link to="#">View Cart</Link></li>
            <li><Link to="#">View Profile</Link></li>
            <li><Link to="/logout">Logout</Link></li>
        </ul>
    )
};

const Navbar = (props) => {
    const { user } = props;
    return (
        <nav className="nav-wrapper grey darken-3">
            <div className="container">
                <Link to="/" className="brand-logo left">ShopCity</Link>
                { (user.isAuthenticated) ? (<SignedOutLinks />):(<SignedInLinks />) }
            </div>
        </nav>
    )
};

const mapStateToProps = (state) => {
    return {
        user: state.auth.user
    }
}

export default connect(mapStateToProps)(Navbar);
