import React from 'react';
import _ from 'lodash';
import {Sparklines, SparklinesLine, SparklinesReferenceLine} from 'react-sparklines';

class Chart extends React.Component
{
    average(data)
    {
        return _.round(_.sum(data)/data.length);
    }

    render ()
    {
        return(

            <div>
                <h3>{this.average(this.props.data)}{this.props.unit}</h3>
                <Sparklines data={this.props.data} >
                    <SparklinesLine color={this.props.color} />
                    <SparklinesReferenceLine type="avg" />
                </Sparklines>
            </div>
        )
    }
}

export default Chart;