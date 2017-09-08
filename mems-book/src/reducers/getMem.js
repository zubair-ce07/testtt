import {GET_MEM, SUCCESS} from "../constants";

export const getMemToUpdate = function (state = null, action) {
    if (action.type == GET_MEM + SUCCESS) {
        return action.payload.data;
    };
    return state;
};
