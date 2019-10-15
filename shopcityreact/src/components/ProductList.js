import React, { Component } from 'react';


class ProductsList extends Component{
    render (){
        const { productsList } = this.props
        const productList = productsList.length ? (
            productsList.map(product => {
                return (
                    <div className="col s12 l3" key={product.retailer_sku}>
                        <div className="card large" >
                            <div className="card-image">
                                <img src={ product.image_url } height='250'></img>                                
                            </div>
                            <div className="card-content">
                                <h6> { product.name }-{ product.brand }</h6>
                                <div className="left-align card-action">
                                    <p>Price: { product.price } { product.currency }</p><br></br>
                                    <a className="btn blue" href="#">View Details</a>
                                </div>
                            </div>
                        </div>
                    </div>
            )})
        ) : (
            <div className="center">No products Found!!</div>
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

export default ProductsList;
