import {updateUserStatusesForMovie} from '../utils/utils';
import {GET_WATCHLIST,REMOVE_FROM_WATCHLIST, LOADING_MORE, LOADED_MORE, FETCHING_WATCHLIST} from '../actions/action_types';


export default function (state = {movies: [], isFetching: true, next: null}, action) {
    let isFetching = false;
    switch (action.type) {
        case FETCHING_WATCHLIST:
            return {movies: [], isFetching: true, next: null};
        case GET_WATCHLIST:
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
        case REMOVE_FROM_WATCHLIST:
            return {movies: updateUserStatusesForMovie(state.movies, action, true), isFetching: false, next: state.next};
        default:
            return state;
    }
}
