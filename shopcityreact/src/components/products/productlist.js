import { connect } from 'react-redux';
import React, { Component } from 'react';
import {withRouter} from 'react-router-dom';


class ProductsList extends Component {
    viewProductDetails = (retailer_sku) => {
        this.props.history.push('/product/' + retailer_sku);
    };

    render (){
        const { products, error } = this.props;
        if (error !== null) {
            return <div className="product-list-error center-align"></div>
        }

        const productList = products ? (
            products.map(product => {
                return (
                    <div className="col s12 l3" key={product.retailer_sku}>
                        <div className="card large" >
                            <div className="card-image">
                                <img src={ product.image_url } style={{height: '250px'}}/>                                
                            </div>
                            <div className="card-content">
                                <h6> { product.name }-{ product.brand }</h6>
                                <div className="left-align card-action">
                                    <p>Price: { product.price } { product.currency }</p><br></br>
                                    <a className="btn blue" onClick={() => {this.viewProductDetails(product.retailer_sku)}}>
                                        View Details
                                    </a>      
                                </div>
                            </div>
                        </div>
                    </div>
            )})
        ) : (
            <div className="center">Loading Products....</div>
        );

        return (
            <div className="products-list container">
                <div className="row">
                    {productList}
                </div>
            </div>
        );
    };
};


const mapStateToProps = (state) => {
    return {
        products: state.product.products,
        currentPage: state.product.currentPage,
        modalOpen: state.modal.modalOpen,
        pending: state.product.pending,
        error: state.product.error
    };
};

export default connect(mapStateToProps, null)(withRouter(ProductsList));
