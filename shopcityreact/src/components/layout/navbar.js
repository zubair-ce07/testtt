import React from 'react';
import { Link} from 'react-router-dom';


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
            <li><Link to="#" className='btn btn-floating pink lighten-1'>AA</Link></li>
        </ul>
    )
};

const Navbar = () => {
    return (
        <nav className="nav-wrapper grey darken-3">
            <div className="container">
                <Link to="/" className="brand-logo left">ShopCity</Link>
                <SignedInLinks />
            </div>
        </nav>
    )
};

export default Navbar;
