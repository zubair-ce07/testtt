import { connect } from 'react-redux';
import React, {Component} from 'react';
import { Link } from 'react-router-dom';

import { checkout } from '../../store/actions/authActions';


class Cart extends Component {
    redirect = () => {
        this.props.history.push('/login');
    };

    renderCartItemsList =  (cartItems) => {
        const cartItemsList = cartItems.length ? (
            cartItems.map(cartItem => {
                return (
                    <div className="row">
                        <div style={{padding: '5%'}} className="card">
                            <Link to={'/product/' + cartItem.product + '/'}>
                                {cartItem.product}
                            </Link>
                            <h6>Quantity: {cartItem.quantity}</h6>
                            <h6>Color: {cartItem.sku_id.split('_')[0]}</h6>
                            <h6>Size: {cartItem.sku_id.split('_')[1]}</h6>
                        </div>
                    </div>
                )})
            ) : (
                <div className="row">
                    <h4>No Products Added to the cart...</h4>
                </div>
            )
        return cartItemsList;
    };

    checkout = () => {
        const { checkout } = this.props;
        checkout();
        this.props.history.push('/checkout');
    };

    render() {
        const { cart, user } = this.props;
        const cartItemsList = this.renderCartItemsList(cart[0].cart_items);

        if ( !user.isAuthenticated ) {
            this.redirect();
        }

        return (
            <div className="container">
                {cartItemsList}
                <div className="row">
                    <Link className="btn waves-effect waves-light" to="/" >
                        Continue Shopping
                    </Link>
                    <button className="btn waves-effect waves-light" onClick={this.checkout}>
                        Proceed To Checkout
                    </button>
                </div>
            </div>
        );
    };
};


const mapDispatchToProps = (dispatch) => {
    return {
        checkout: () => dispatch(checkout())
    };
};


const mapStateToProps = (state) => {
    return {
        user: state.auth.user,
        cart: state.auth.cart
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(Cart);
