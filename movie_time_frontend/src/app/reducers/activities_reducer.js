import {updateUserStatusesInActivities} from '../utils/utils';
import {FETCH_ACTIVITIES, FETCH_USER_ACTIVITIES, FETCHING_ACTIVITIES, ADD_TO_WATCHLIST, REMOVE_FROM_WATCHLIST, LOADED_MORE, LOADING_MORE} from '../actions/action_types';


export default function (state = {activities: [], isFetching: true, next: null}, action) {
    let isFetching = false;
    switch (action.type) {
        case FETCHING_ACTIVITIES:
            return{activities: [], isFetching: true, next: null};
        case FETCH_USER_ACTIVITIES:
        case FETCH_ACTIVITIES:
            return {activities: action.payload.data.results, isFetching: false, next: action.payload.data.next};
        case LOADING_MORE:
            if (state.next === action.payload) isFetching = true;
            return {activities: state.activities, isFetching: isFetching, next: state.next};
        case LOADED_MORE:
            if (state.next === action.payload.config.url)
                return {
                    activities: state.activities.concat(action.payload.data.results),
                    isFetching: false,
                    next: action.payload.data.next
                };
            return state;
        case ADD_TO_WATCHLIST:
        case REMOVE_FROM_WATCHLIST:
            return {activities: updateUserStatusesInActivities(state.activities, action), isFetching: false, next: state.next};
        default:
            return state;
    }
}
