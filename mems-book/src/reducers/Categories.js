import {ADD_CATEGORY, GET_CATEGORIES, SUCCESS} from "../constants";

export const userCategories = function (state = [], action) {
    if (action.type === ADD_CATEGORY + SUCCESS) {
        return [action.payload.data, ...state];
    } else if (action.type === GET_CATEGORIES + SUCCESS) {
        return action.payload.data;
    }
    return state;
};

