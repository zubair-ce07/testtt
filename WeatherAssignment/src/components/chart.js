import _ from "lodash";
import React from 'react';
import {Sparklines, SparklinesLine, SparklinesSpots, SparklinesReferenceLine} from 'react-sparklines';

export default props => {
    return(
        <div>
            <Sparklines height={80} width={100} data={props.data}>
                <SparklinesLine color= {props.color}/>
                <SparklinesSpots style={{ fill: (props.color) }}/>
                <SparklinesReferenceLine type="avg" />
            </Sparklines>
            <strong>Mean: {mean(props.data)} {props.units}</strong>
        </div>
    );
}//function

function mean(data) {
  return _.round(_.sum(data) / data.length);
}
