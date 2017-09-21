import {updateUserStatusesForMovie} from '../utils/utils';
import {
    EXPLORE_WITH_GENRE,
    REQUESTING_WITH_GENRE,
    ADD_TO_WATCHLIST,
    REMOVE_FROM_WATCHLIST,
    LOADING_MORE,
    LOADED_MORE
} from '../actions/action_types';


export default function (state = {movies: [], isFetching: false, next: null}, action) {
    switch (action.type) {
        case REQUESTING_WITH_GENRE:
            return {movies: [], isFetching: true, next: null};
        case EXPLORE_WITH_GENRE:
            return {movies: action.payload.data.results, isFetching: false, next: action.payload.data.next};
        case LOADING_MORE:
            return {movies: state.movies, isFetching: true, next: state.next};
        case LOADED_MORE:
            return {movies: state.movies.concat(action.payload.data.results), isFetching: false, next: action.payload.data.next};
        case ADD_TO_WATCHLIST:
        case REMOVE_FROM_WATCHLIST:
            return {movies: updateUserStatusesForMovie(state.movies, action), isFetching: false, next: state.next};
        default:
            return state;
    }
}
