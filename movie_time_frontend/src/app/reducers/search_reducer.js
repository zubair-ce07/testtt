import {updateUserStatusesForMovie} from '../utils/utils';
import {SEARCH_MOVIE, SEARCHING, ADD_TO_WATCHLIST, REMOVE_FROM_WATCHLIST, SEARCH_USER} from '../actions/action_types';


export default function (state = {results: [], isFetching: false, type:null}, action) {
    switch (action.type) {
        case SEARCHING:
            return {results: [], isFetching: true, type:null};
        case SEARCH_MOVIE:
            return {results: action.payload.data, isFetching: false, type:'movies'};
        case SEARCH_USER:
            return {results: action.payload.data.results, isFetching:false, type:'users'};
        case ADD_TO_WATCHLIST:
        case REMOVE_FROM_WATCHLIST:
            return {results: updateUserStatusesForMovie(state.results, action), isFetching: false, type:'movies'};
        default:
            return state;
    }
}
