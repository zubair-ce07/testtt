import React from 'react'
import PropTypes from 'prop-types'
import {Link} from 'react-router-dom'
import {Col, Button} from 'react-bootstrap/lib'
import {getOrDeleteProduct} from '../authentication/auth'

var toastr = require('toastr')
class ListBrandItem extends React.Component {
    render() {
        const thumbStyle = {
            // height: '437px',
            width: '235px'
        }
        const image = this.props.product.images.length > 0 ? this.props.product.images[0].image_url:'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ6jvCc5wDOGnJm6HOKRhgnm1JByfEZkWY0RWK1Ji8R8PMQaqEvSsFih52R'
        return (

            <Col md={3}>
                <div className="thumbnail responsive" style={thumbStyle}>
                    <Link to={'/product/' + this.props.product.pk + '-' + this.props.product.product_name}>
                        <img
                            src={image}
                            alt="brand"
                            style={{
                            height: '300px'
                        }}/>
                    </Link>
                    <div className="caption">
                        <p className="text-center">
                            {this.props.product.product_name}
                        </p>

                        <p className="text-center">
                            {this.props.product.skus_set.length > 0
                                ? '$' + this.props.product.skus_set[0].price
                                : 'N\\A'}
                        </p>
                        <Link to={'/product/update/'+this.props.product.pk}>
                            <Button bsStyle='primary'> Update! </Button>
                        </Link>
                        <Button bsStyle='danger' className='pull-right' onClick={() => getOrDeleteProduct(this.props.product.pk, 'delete', () => toastr.success('brand deleted successfully!'))}> Delete! </Button>
                    </div>
                </div>
            </Col>
        )
    }
}

ListBrandItem.propTypes = {
    product: PropTypes.object.isRequired,
}

export default ListBrandItem
