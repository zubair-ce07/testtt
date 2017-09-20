import {SET_ACTIVE_PAGE} from '../actions/action_types';


export default function (state = null, action) {
    switch (action.type) {
        case SET_ACTIVE_PAGE:
            return action.payload;
        default:
            return state;
    }
}
