import {FETCH_MOVIE} from '../actions/index';

export default function (state = null, action) {
    switch (action.type) {
        case FETCH_MOVIE:
            return action.payload;
        default:
            return state;
    }
}
