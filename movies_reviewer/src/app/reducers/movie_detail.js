import {FETCH_MOVIE} from '../actions/movies_actions';

export default function (state = null, action) {
    switch (action.type) {
        case FETCH_MOVIE:
            return action.payload;
        default:
            return state;
    }
}
