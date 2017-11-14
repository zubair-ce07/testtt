import React from 'react'
import PropTypes from 'prop-types'
import List from './ListTiles'

class GridInstance extends React.Component{
    render(){
        return(
            <div className="container">
                <List itemList={this.props.itemList} _handleDelete={this.props._handleDelete} name={this.props.name}/>
            </div>
        )
    }
}

GridInstance.PropType = {
    itemList: PropTypes.array.isRequired,
    name: PropTypes.string.isRequired
}

export default GridInstance
