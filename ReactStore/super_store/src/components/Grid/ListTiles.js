import React from 'react'
import {Grid, Row} from 'react-bootstrap/lib'

import ListBrandItem from './ListBrandItem'
import ListProductItem from './ListProductItem'

const List = (props) => {

    var List = props.itemList.reduce(function(accumulator,currentValue, currentIndex, array){
        if(accumulator[accumulator.length - 1].length === 4){
            accumulator.push([])
        }
        accumulator[accumulator.length - 1].push(
            (props.name === 'brands' ? <ListBrandItem brand={currentValue} key={currentIndex} /> : <ListProductItem product={currentValue} key={currentIndex}/>))
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
