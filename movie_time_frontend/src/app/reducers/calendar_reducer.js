import {updateUserStatusesForMovie} from '../utils/utils';
import {
    EXPLORE_WITH_DATE,
    REQUESTING_WITH_DATE,
    ADD_TO_WATCHLIST,
    REMOVE_FROM_WATCHLIST,
    LOADING_MORE,
    LOADED_MORE
} from '../actions/action_types';


export default function (state = {movies: [], isFetching: false, next: null}, action) {
    let isFetching = false;
    switch (action.type) {
        case REQUESTING_WITH_DATE:
            return {movies: [], isFetching: true, next: null};
        case EXPLORE_WITH_DATE:
            return {movies: action.payload.data.results, isFetching: false, next: action.payload.data.next};
        case LOADING_MORE:
            if (state.next === action.payload) isFetching = true;
            return {movies: state.movies, isFetching: isFetching, next: state.next};
        case LOADED_MORE:
            if (state.next === action.payload.config.url)
                return {
                    movies: state.movies.concat(action.payload.data.results),
                    isFetching: false,
                    next: action.payload.data.next
                };
            return state;
        case ADD_TO_WATCHLIST:
        case REMOVE_FROM_WATCHLIST:
            return {movies: updateUserStatusesForMovie(state.movies, action), isFetching: false, next: state.next};
        default:
            return state;
    }
}
