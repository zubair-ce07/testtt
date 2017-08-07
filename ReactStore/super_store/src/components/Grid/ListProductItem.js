import React from 'react'
import {Link} from 'react-router-dom'
import {Col} from 'react-bootstrap/lib'

const ListBrandItem = (props) => {
    var thumbStyle = {
        height: '400px',
        width: '235px'
    }
    var image = props.product.images[0].image_url
    return(

        <Col md={3}>
            <div className="thumbnail" style={thumbStyle}>
                <Link to={'/product/'+props.product.pk+'-'+props.product.product_name}>
                    <img src={image} alt="brand" style={{height: '300px'}}/>
                </Link>
                <div className="caption">
                    <p className="text-center">
                            {props.product.product_name}
                    </p>
                    <p className="text-center">
                            {props.product.skus_set.length>0 ?
                            '$'+props.product.skus_set[0].price:'N\\A'}
                    </p>
                </div>
            </div>
        </Col>
    )
}

export default ListBrandItem
