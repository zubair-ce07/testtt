import React from 'react'
import PropTypes from 'prop-types'
import {Link} from 'react-router-dom'
import {Col} from 'react-bootstrap/lib'

class ListBrandItem extends React.Component {
    render() {

        const thumbStyle = {
            height: '400px',
            width: '235px'
        }
        const image = this.props.product.images[0].image_url
        return (

            <Col md={3}>
                <div className="thumbnail" style={thumbStyle}>
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
