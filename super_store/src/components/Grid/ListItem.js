import React from 'react'
import {Col} from 'react-bootstrap/lib'

const ListItem = (props) => {
    var thumbStyle = {
        height: '400px',
        width: '235px'
    }
    return(
        <Col md={3}>
            <div className="thumbnail" style={thumbStyle}>
                <a href="">
                    <img src={props.brand.image_icon} alt="brand image" style={{height: '300px'}}/>
                </a>
                <div className="caption">
                    <p className="text-center">
                        <a href="">
                            {props.brand.name}
                        </a>
                    </p>
                    <p className="text-center">
                        <a href={props.brand.brand_link}>
                            Go To Brand's Page
                        </a>
                    </p>
                </div>
            </div>
        </Col>
    )
}

export default ListItem
