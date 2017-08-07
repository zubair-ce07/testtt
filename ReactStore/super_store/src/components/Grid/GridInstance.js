import React from 'react'
import List from './ListTiles'

const GridInstance = (props) => {


    return(
        <div className="container">
            <List itemList={props.itemList} name={props.name}/>
        </div>
    )
}

export default GridInstance
