import React from 'react'
import PropTypes from 'prop-types'

import Navigation from './Common/Header'
import Footer from './Common/Footer'
import GridInstance from './Grid/GridInstance'
import {Route} from 'react-router-dom'
import {loggedIn, listItems} from './authentication/auth'


class SelectedBrand extends React.Component {
    constructor(){
        super()
        this.state = {
            products: [],
            brand: {}
        }
    }
    componentDidMount(){
        if (!loggedIn()) {
            this.props.history.push('/app/login/')
        }

        const that = this
        listItems("http://localhost:8000/api/brand/products/"+this.props.match.params.name, (jsonData) => {
            var products = []
            console.log(jsonData)
            if(jsonData.results[0].product.length > 0){
                jsonData.results[0].product.forEach(function(element) {
                    products.push(element)
                }, this);

            }
            that.setState({
                    products,
                    brand: jsonData.results[0]
            })

        })
    }

    render(){
        return(
            <div>
                <Route component={Navigation} />
                <h1 className="text-center">
                    Super Store's reknowned Products of {this.state.brand.name}
                </h1>
                {(this.state.products.length > 0 ?
                    <GridInstance itemList={this.state.products} name='products'/>:
                    <div className='text-center text-danger'>
                        <h1> OOPS! </h1>
                        <p>No products exist for this Brand</p>
                    </div>
                )}
                <Footer />
            </div>
        )
    }
}

SelectedBrand.propTypes = {
    history: PropTypes.object.isRequired,
    match: PropTypes.object.isRequired
}

export default SelectedBrand
