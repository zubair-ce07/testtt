import { FETCH_SEARCH_NEWS, FETCH_NEWS_BY_CATEGORY_NAME } from '../actions';
import _ from 'lodash'

export default function(state = [], action) {
    switch(action.type) {
        case FETCH_SEARCH_NEWS:
            return action.payload.data;
          case FETCH_NEWS_BY_CATEGORY_NAME:
            return action.payload.data;
        default:
            return state;
    }
}
