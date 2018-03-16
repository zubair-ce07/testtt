



import * as types from '../actions/actionTypes';
import initialState from './initialState';
import _ from 'underscore'


export default function weatherReducer(state = initialState.config, action) {
    switch(action.type) {
        case types.LOAD_WEATHER_SUCCESS: {
            console.log(action)
            console.log(state);

            return Object.assign({}, state, {
                series: state.series.map((item, index) => {
                    //if(item.name==='Temperature'){
                        return Object.assign({}, item, {
                            data: item.data.concat(_.map(action.weather.list, function (obj) {
                                    return {name: action.weather.city.name, y: obj.main[item.name]}
                                })
                            )

                        })
                  //  }


                    return item
                }),
                xAxis:state.xAxis.map((axis, index) => {
                    //if(item.name==='Temperature'){
                    return Object.assign({}, axis, {
                        categories:axis.categories.concat(_.pluck(action.weather.list,'dt_txt'))

                    })


                    return axis
                })

            })
        }

        default:
            return state;
    }
}
