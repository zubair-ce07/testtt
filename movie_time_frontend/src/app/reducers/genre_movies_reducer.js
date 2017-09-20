import {updateUserStatusesForMovie} from '../utils/utils';
import {EXPLORE_WITH_GENRE, REQUESTING_WITH_GENRE, ADD_TO_WATCHLIST, REMOVE_FROM_WATCHLIST} from '../actions/action_types';


export default function (state = {movies: [], isFetching: false}, action) {
    switch (action.type) {
        case REQUESTING_WITH_GENRE:
            return {movies: [], isFetching: true};
        case EXPLORE_WITH_GENRE:
            return {movies: action.payload.data.results, isFetching: false};
        case ADD_TO_WATCHLIST:
        case REMOVE_FROM_WATCHLIST:
            return {movies: updateUserStatusesForMovie(state.movies, action), isFetching: false};
        default:
            return state;
    }
}
