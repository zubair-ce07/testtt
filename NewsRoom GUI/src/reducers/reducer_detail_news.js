import { FETCH_NEWS_DETAIL } from '../actions';
import _ from 'lodash'

export default function(state = {}, action) {
    switch(action.type) {
        case FETCH_NEWS_DETAIL:
            return action.payload.data;
        default:
            return state;
    }
}