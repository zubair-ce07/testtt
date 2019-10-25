import React from 'react';
import { Link} from 'react-router-dom';
import { connect } from 'react-redux';


const SignedOutLinks = () => {
    return (
        <ul className="right">
            <li><Link to="#">View Cart</Link></li>
            <li><Link to="/register">Register</Link></li>
            <li><Link to="/login">Login</Link></li>
        </ul>
    )
};

const SignedInAdminLinks = () => {
    return (
        <ul className="right">
            <li><Link to="/profile">Profile</Link></li>
            <li><Link to="/logout">Logout</Link></li>
        </ul>
    )
};

const SignedInCustomerLinks = () => {
    return (
        <ul className="right">
            <li><Link to="#">View Cart</Link></li>
            <li><Link to="/profile">View Profile</Link></li>
            <li><Link to="/logout">Logout</Link></li>
        </ul>
    )
};

const Navbar = (props) => {
    const { user } = props;
    if (user.isAuthenticated && !user.isSuperUser) {
        var navLinks = <SignedInCustomerLinks />
    } else if (user.isAuthenticated && user.isSuperUser) {
        var navLinks = <SignedInAdminLinks />
    } else {
        var navLinks = <SignedOutLinks />
    }
    return (
        <nav className="nav-wrapper grey darken-3">
            <div className="container">
                <Link to="/" className="brand-logo left">ShopCity</Link>
                { navLinks }
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
