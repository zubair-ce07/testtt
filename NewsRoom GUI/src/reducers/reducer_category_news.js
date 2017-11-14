import { FETCH_NEWS_CATEGORIES } from '../actions';
import _ from 'lodash'


export default function(state = {}, action) {
    switch(action.type) {
        case FETCH_NEWS_CATEGORIES:
            return _(action.payload.data).groupBy(object => object.category.name).map((value, key) => ({category: key, news: value})).value() 
        default:
            return state;
    }
}