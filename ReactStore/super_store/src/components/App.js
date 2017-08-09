import React from 'react'
import PropTypes from 'prop-types'
import {Route} from 'react-router-dom'

import Navigation from './Common/Header'
import Footer from './Common/Footer'
import GridInstance from './Grid/GridInstance'
import {loggedIn, listItems} from './authentication/auth'
import AddBrandForm from './AddBrandForm'

class App extends React.Component {
    constructor(){
        super()
        this.state = {
            brands: [],
            products: []
        }
    }
    componentDidMount(){
        if (!loggedIn()) {
            this.props.history.push('/app/login/')
        }
        const that = this
        listItems("http://localhost:8000/api/brand/list", (jsonData) => {
            var brands = []
            if(jsonData.results){
                jsonData.results.forEach(function(element) {
                    brands.push(element)
                }, this);
                that.setState({
                    brands
                })
            }
        })
        listItems("http://localhost:8000/api/products/", (jsonData) => {
            var products = []
            if(jsonData.results){
                jsonData.results.forEach(function(element) {
                    products.push(element)
                }, this);
                that.setState({
                    products
                })
            }

        })
    }

    render(){
        return(
            <div>
                <Route component={Navigation} />
                <h1 className="text-center">
                    Super Store's reknowned {this.props.match.params.name}
                </h1>
                {(this.props.match.params.name === 'brands' ? <AddBrandForm />:'')}
                <GridInstance itemList={this.state[this.props.match.params.name]} name={this.props.match.params.name}/>
                <Footer />
            </div>
        )
    }
}

App.propTypes = {
    history: PropTypes.object.isRequired,
    match: PropTypes.object.isRequired
}

export default App
