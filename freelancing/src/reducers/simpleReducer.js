import { SIMPLE_ACTION } from "../actions/types";

export const simpleReducer = (state = {}, action) => {
    switch (action.type) {
        case SIMPLE_ACTION:
            console.log("simple action fired", action)
            return {
                result: action.payload
            }
        default:
            return state
    }
}