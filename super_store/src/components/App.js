import React from 'react'

import Navigation from './Common/Header'
import Footer from './Common/Footer'
import GridInstance from './Grid/GridInstance'
import {Route} from 'react-router-dom'
import {loggedIn, listBrands} from './authentication/auth'


class App extends React.Component {
    constructor(){
        super()
        this.state = {
            brands: []
        }
    }
    componentWillMount(){
        if (!loggedIn()) {
            this.props.history.push('/app/login/')
        }
        const that = this
        listBrands((jsonData) => {
            console.log(jsonData.results)

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
    }

    render(){
        return(
            <div>
                <Route component={Navigation} />
                <h1 className="text-center">
                    Super Store's reknowned Brands
                </h1>
                <GridInstance brands={this.state.brands} />
                <Footer />
            </div>
        )
    }
}

export default App
