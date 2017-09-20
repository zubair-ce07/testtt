import {updateUserStatusesForMovie} from '../utils/utils';
import {GET_WATCHED_LIST, REMOVE_FROM_WATCHLIST} from '../actions/action_types';


export default function (state = [], action) {
    switch (action.type) {
        case GET_WATCHED_LIST:
            return action.payload.data.results;
        case REMOVE_FROM_WATCHLIST:
            return updateUserStatusesForMovie(state, action, true);
        default:
            return state;
    }
}
