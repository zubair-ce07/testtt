import React, { Component } from 'react';
import {withRouter} from 'react-router-dom';
import { connect } from 'react-redux';


class ProductsList extends Component{
    viewProductDetails = (retailer_sku) => {
        this.props.history.push('/product/' + retailer_sku);
    };
    render (){
        const { products, pending, error } = this.props;
        console.log("Products List", products)
        if (error !== null) {
            return <div className="product-list-error center-align"></div>
        }
        const productList = products ? (
            products.map(product => {
                return (
                    <div className="col s12 l3" key={product.retailer_sku}>
                        <div className="card large" >
                            <div className="card-image">
                                <img alt="" style={{height: '250px'}} src="https://images.pexels.com/photos/67636/rose-blue-flower-rose-blooms-67636.jpeg?auto=compress&cs=tinysrgb&h=750&w=1260"></img>
                                {/* <img src={ product.image_url } height='250'></img>                                 */}
                            </div>
                            <div className="card-content">
                                <h6> { product.name }-{ product.brand }</h6>
                                <div className="left-align card-action">
                                    <p>Price: { product.price } { product.currency }</p><br></br>
                                    <a className="btn blue" onClick={() => {this.viewProductDetails(product.retailer_sku)}}>View Details</a>      
                                </div>
                            </div>
                        </div>
                    </div>
            )})
        ) : (
            <div className="center">Loading Products....</div>
        )
        return (
            <div className="products-list container">
                <div className="row">
                    {productList}
                </div>
            </div>
        ) 

}
};

const mapStateToProps = (state) => {
    return {
        products: state.product.products,
        currentPage: state.product.currentPage,
        modalOpen: state.modal.modalOpen,
        pending: state.product.pending,
        error: state.product.error
    }
}

export default connect(mapStateToProps, null)(withRouter(ProductsList));
