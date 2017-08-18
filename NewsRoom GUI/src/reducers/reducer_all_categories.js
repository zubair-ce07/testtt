import { ALL_CATEGORIES } from '../actions';

export default function(state = [], action) {
    switch(action.type) {
        case ALL_CATEGORIES:
            console.log("All Categories", action.payload.data);
            return action.payload.data;
        default:
            return state;
    }
}