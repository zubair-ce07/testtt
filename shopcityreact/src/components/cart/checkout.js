import React from 'react';
import { Link } from 'react-router-dom';


const Checkout = (props) => {

    return (
        <div className="container">
            <div className="card" style={{padding: '5%'}}>
                <h5>Thank You for Shopping with us.</h5>
                <Link to="/" className="btn waves-effect waves-light">
                    Back to Homepage
                </Link>
            </div>
        </div>
    )
};

export default Checkout;
