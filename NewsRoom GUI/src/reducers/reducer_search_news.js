import { FETCH_SEARCH_NEWS } from '../actions';
import _ from 'lodash'

export default function(state = [], action) {
    switch(action.type) {
        case FETCH_SEARCH_NEWS:
            return action.payload.data;
        default:
            return state;
    }
}