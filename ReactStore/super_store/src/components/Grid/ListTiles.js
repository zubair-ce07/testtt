import React from 'react'
import PropTypes from 'prop-types'
import {Grid, Row} from 'react-bootstrap/lib'

import ListBrandItem from './ListBrandItem'
import ListProductItem from './ListProductItem'

class List extends React.Component {
    render() {

        var List = this.props.itemList.reduce((accumulator, currentValue, currentIndex, array) => {
                if (accumulator[accumulator.length - 1].length === 4) {
                    accumulator.push([])
                }
                accumulator[accumulator.length - 1].push((this.props.name === 'brands'
                    ? <ListBrandItem _handleDelete={this.props._handleDelete} brand={currentValue} key={currentIndex}/>
                    : <ListProductItem product={currentValue} key={currentIndex}/>))
                return accumulator
            },
            [[]]
        )

        List = List.map((row, index) => {
            return <Row className="show-grid" key={index}>{row}</Row>
        })

        return (
            <Grid>
                {List}
            </Grid>
        )
    }
}

List.propTypes = {
    itemList: PropTypes.array.isRequired,
    name: PropTypes.string.isRequired
}

export default List
