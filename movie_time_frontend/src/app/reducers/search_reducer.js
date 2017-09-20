import {updateUserStatusesForMovie} from '../utils/utils';
import {SEARCH_MOVIE, SEARCHING_MOVIE, ADD_TO_WATCHLIST, REMOVE_FROM_WATCHLIST} from '../actions/action_types';


export default function (state = {movies: [], isFetching: false}, action) {
    switch (action.type) {
        case SEARCHING_MOVIE:
            return {movies: [], isFetching: true};
        case SEARCH_MOVIE:
            return {movies: action.payload.data, isFetching: false};
        case ADD_TO_WATCHLIST:
        case REMOVE_FROM_WATCHLIST:
            return {movies: updateUserStatusesForMovie(state.movies, action), isFetching: false};
        default:
            return state;
    }
}
