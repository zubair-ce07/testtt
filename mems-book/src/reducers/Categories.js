import { ADD_CATEGORY, GET_CATEGORIES} from '../constants'

export const userCategories = function (state=[], action) {
    if (action.type === ADD_CATEGORY+'_FULFILLED'){
        return [action.payload.data, ...state] ;
    } else if (action.type === GET_CATEGORIES+'_FULFILLED') {
        return action.payload.data;
    }
    return state;
}

