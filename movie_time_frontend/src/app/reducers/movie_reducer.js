import _ from 'lodash';
import {
    FETCH_MOVIE_DETAIL,
    FETCHING_MOVIE,
    UPDATE_WATCHLIST,
    RATE_MOVIE,
    ADD_TO_WATCHLIST,
    REMOVE_FROM_WATCHLIST,
    VOTE_ACTOR
} from '../actions/action_types';


export default function (state = {movie: null, isFetching: true}, action) {
    switch (action.type) {
        case FETCHING_MOVIE:
            return {movie: null, isFetching: true};

        case FETCH_MOVIE_DETAIL:
            return {movie: action.payload.data, isFetching: false};

        case UPDATE_WATCHLIST:
        case RATE_MOVIE:
        case ADD_TO_WATCHLIST:
        case REMOVE_FROM_WATCHLIST:
            if(state.movie !== null && state.movie.id === action.payload.data.movie)
                state.movie.user_statuses = action.payload.data;
            return {movie: state.movie, isFetching: false};

        case VOTE_ACTOR:
            if(state.movie !== null && state.movie.id === action.payload.data.movie) {

                _.map(state.movie.cast, role => {
                    if(role.id === state.movie.user_statuses.best_actor) role.votes -= 1;
                    if(role.id === action.payload.data.best_actor) role.votes += 1;
                });

                state.movie.user_statuses = action.payload.data;
            }
            return {movie: state.movie, isFetching: false};

        default:
            return state;
    }
}
