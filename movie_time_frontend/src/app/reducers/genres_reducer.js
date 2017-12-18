import {GET_GENRES} from '../actions/action_types';


export default function (state = [], action) {
    switch (action.type) {
        case GET_GENRES:
            return action.payload.data.results;
        default:
            return state;
    }
}
