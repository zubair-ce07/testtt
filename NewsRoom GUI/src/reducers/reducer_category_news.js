import { FETCH_NEWS_CATEGORIES } from '../actions';
import _ from 'lodash'

export default function(state = {}, action) {
    switch(action.type) {
        case FETCH_NEWS_CATEGORIES:
            console.log('other_news before conversion: ',action.payload.data)
            const result = _(action.payload.data).groupBy(object => object.category.name).map((value, key) => ({category: key, news: value})).value() 
            console.log('other_news: ',result)
            return result;
        default:
            return state;
    }
}