import { GET_PUBLIC_MEMS, DELETE_MEM} from '../constants'

export const publicMems = function (state=[], action) {
    if (action.type === GET_PUBLIC_MEMS+'_FULFILLED'){
        return action.payload.data;
    }else if (action.type === DELETE_MEM+'_FULFILLED'){
        let id = action.payload.data.id;
        var newState = [];
         for (let i in state)
         {
             if (state[i].id != id)
             {
                newState.push(state[i]);
             }
         }
         return newState

    }
    return state;
}
