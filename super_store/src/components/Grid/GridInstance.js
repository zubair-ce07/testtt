import React from 'react'

import List from './ListTiles'

const GridInstance = (props) => {


    return(
        <div className="container">
                <List List={props.brands} />
        </div>
    )
}

export default GridInstance
