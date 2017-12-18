import {ADD_MEM, DELETE_MEM, GET_USERS_MEMS, SUCCESS} from "../constants";

export const userMems = function (state = [], action) {
    if (action.type === GET_USERS_MEMS + SUCCESS) {
        return action.payload.data;
    } else if (action.type === ADD_MEM + SUCCESS) {
        return [action.payload.data, ...state]
    } else if (action.type === DELETE_MEM + SUCCESS) {
        let id = action.payload.data.id;
        return state.map((mem) => {
            if (mem.id != id) {
                return mem;
            }
        });
    };
    return state;
};
