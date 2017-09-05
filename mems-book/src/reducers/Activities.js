import { GET_USER_ACTIVITIES} from '../constants'

export const userActivities = function (state=[], action) {
    if (action.type === GET_USER_ACTIVITIES+'_FULFILLED'){
        return action.payload.data;
    }
    return state;
}
