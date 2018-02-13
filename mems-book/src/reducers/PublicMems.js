import {DELETE_MEM, GET_PUBLIC_MEMS, SUCCESS} from "../constants";

export const publicMems = function (state = [], action) {
    if (action.type === GET_PUBLIC_MEMS + SUCCESS) {
        return action.payload.data;
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
