import {GET_USER_ACTIVITIES, SUCCESS} from "../constants";

export const userActivities = function (state = [], action) {
    if (action.type === GET_USER_ACTIVITIES + SUCCESS) {
        return action.payload.data;
    };
    return state;
};
