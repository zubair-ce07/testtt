import {FETCH_ACTOR} from '../actions/actors_actions';

export default function (state = null, action) {
    switch (action.type) {
        case FETCH_ACTOR:
            return action.payload;
        default:
            return state;
    }
}
