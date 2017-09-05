import {GET_MEM} from '../constants'

export const getMemToUpdate = function (state=null, action) {
    if (action.type == GET_MEM+'_FULFILLED') {
            return action.payload.data;
    }
    return state;
}
