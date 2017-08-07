import React from 'react'
import {Link} from 'react-router-dom'
import {Col} from 'react-bootstrap/lib'

const ListBrandItem = (props) => {
    var thumbStyle = {
        height: '400px',
        width: '235px'
    }
    return(
        <Col md={3}>
            <div className='thumbnail' style={thumbStyle}>
                <Link to={'/brand/'+props.brand.name}>
                    <img src={props.brand.image_icon} alt='brand' style={{height: '300px'}}/>
                </Link>
                <div className='caption'>
                    <p className='text-center'>
                            {props.brand.name}
                    </p>
                    <p className='text-center'>
                        <a href={props.brand.brand_link}>
                            Go To Brand's Page
                        </a>
                    </p>
                </div>
            </div>
        </Col>
    )
}

export default ListBrandItem
