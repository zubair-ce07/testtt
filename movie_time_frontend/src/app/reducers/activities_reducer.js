import _ from 'lodash';
import {FETCH_ACTIVITIES, ADD_TO_WATCHLIST, REMOVE_FROM_WATCHLIST} from '../actions/action_types';


export default function (state = [], action) {
    const newState = [];
    switch (action.type) {
        case FETCH_ACTIVITIES:
            return action.payload.data.results;
        case ADD_TO_WATCHLIST:
            _.map(state, activity => {
                if(activity.movie.id === action.payload.data.movie) activity.movie.user_statuses = action.payload.data;
                newState.push(activity);
            });
            return newState;
        case REMOVE_FROM_WATCHLIST:
            _.map(state, activity => {
                if(activity.movie.id === action.payload.data.movie) activity.movie.user_statuses = action.payload.data;
                newState.push(activity);
            });
            return newState;
        default:
            return state;
    }
}
