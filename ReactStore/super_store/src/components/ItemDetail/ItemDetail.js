import React from 'react'
import {Route} from 'react-router-dom'

import {Image, Row, Col, Table} from 'react-bootstrap/lib'
import Navigation from '../Common/Header'
import {loggedIn, listItems} from '../authentication/auth'

class ItemDetail extends React.Component{
    constructor(){
        super()
        this.state = {
            product: {},
            price: '',
            imageBoxes: [],
            skus: []
        }

    }
    componentWillMount(){
        if (!loggedIn()) {
            this.props.history.push('/app/login/')
        }
        const that = this
        listItems("http://localhost:8000/api/product/"+this.props.match.params.id, (jsonData) => {


            var imageBoxes = jsonData.images.map(function(val, index){
                return <Col md={12} key={index}> <Image src={val.image_url} key={index} responsive style={{height: '400px', margin: '0 auto'}} /></Col>

            })
            var skus = jsonData.skus_set.map(function(val, index){
                return <tr key={index}><th>{val.color}</th><th>{val.size === null ? '--':val.size}</th><th>{val.price === null ? '--': val.price}</th><th>{val.availability ? 'available':'out of stock'}</th></tr>
            })
            let price = jsonData.skus_set[0].price
            console.log(jsonData.skus_set)
            that.setState({
                product: jsonData,
                imageBoxes,
                price,
                skus
            })
        })
    }

    render(){
        return(

            <div>
                <Route component={Navigation} />
                <p>
                    Category: {this.state.product.category}
                </p>
                <p>
                    NAME: {this.state.product.product_name}
                </p>
                <p>
                    PRICE: ${this.state.price}
                </p>
                SKUS:
                <Table striped bordered condensed hover>
                    <thead>
                        <tr>
                            <th>
                                Color
                            </th>
                            <th>
                                Size
                            </th>
                            <th>
                                Price
                            </th>
                            <th>
                                Availability
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {this.state.skus}
                    </tbody>
                </Table>
                <Row>
                    {this.state.imageBoxes}
                </Row>

            </div>
        )
    }
}

export default ItemDetail
