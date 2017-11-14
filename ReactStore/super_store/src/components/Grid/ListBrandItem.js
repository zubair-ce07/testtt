import React from 'react'
import PropTypes from 'prop-types'
import {Link} from 'react-router-dom'
import {Col, Button} from 'react-bootstrap/lib'

class ListBrandItem extends React.Component {
    render() {
        const thumbStyle = {
            height: '415px',
            width: '235px'
        }
        const brand = this.props.brand
        return (
            <Col md={3}>
                <div className='thumbnail' style={thumbStyle}>
                    <Link to={'/brand/' + this.props.brand.name}>
                        <img
                            src={this.props.brand.image_icon}
                            alt='brand'
                            style={{
                            height: '300px'
                        }}/>
                    </Link>
                    <div className='caption'>
                        <p className='text-center'>
                            {this.props.brand.name}
                        </p>
                        <p className='text-center'>
                            <a href={this.props.brand.brand_link}>
                                Go To Brand's Page
                            </a>
                        </p>
                        <Link to={'/brand/update/'+this.props.brand.pk}>
                            <Button bsStyle='primary'> Update! </Button>
                        </Link>
                        <Button bsStyle='danger' className='pull-right' onClick={() => this.props._handleDelete(brand.pk)} > Delete! </Button>
                    </div>
                </div>
            </Col>
        )
    }
}

ListBrandItem.propTypes = {
    brand: PropTypes.object.isRequired
}

export default ListBrandItem
