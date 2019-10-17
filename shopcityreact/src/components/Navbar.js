import React from 'react';
import { Link} from 'react-router-dom';


const Navbar = () => {
    return (
        <nav className="nav-wrapper grey darken-3">
            <div className="container">
                <Link to="/" className="brand-logo left">ShopCity</Link>
                <ul className="right">
                    <li><Link to="/home">View Cart</Link></li>
                    <li><Link to="/login">Login</Link></li>
                    <li><Link to="/register">Register</Link></li>
                </ul>
            </div>
        </nav>
    )
};

export default Navbar;
