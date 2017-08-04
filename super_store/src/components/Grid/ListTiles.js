import React from 'react'
import {Grid, Row} from 'react-bootstrap/lib'

import ListItem from './ListItem'

const List = (props) => {

    var List = props.List.map(function(brand, index){
        return <ListItem brand={brand} key={index} />
    })
    List = List.reduce(function(accumulator,currentValue, currentIndex, array){
        if(accumulator[accumulator.length - 1].length === 4){
            accumulator.push([])
        }
        accumulator[accumulator.length - 1].push(currentValue)
        return accumulator
    }, [[],])

    List = List.map(function(row, index){
        return <Row className="show-grid" key={index}>{row}</Row>
    })
    return(
        <Grid>
            {List}
        </Grid>
    )
}

export default List
