import React, { Component } from 'react';
import ProductsList from './ProductList';


class ProductsFilter extends Component{

    render (){
        const { productsList } = this.props;

        var categories = []
        for (const product of productsList) {
          console.log(product.categories[0].category)
        }
        return (
            <div>
              {categories}
            </div>
          )
        // for (let product of productsList) {
        //     console.log(product['categories'])
        // }
        // return (
        //     <div className="products-list container">
        //         <div className="row">
        //         </div>
        //     </div>
        // ) 

}
};

export default ProductsFilter;
