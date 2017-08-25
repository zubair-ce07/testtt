import _ from 'lodash';

import {FETCH_REVIEWS, CREATE_REVIEW} from '../actions/reviews_actions';

export default function (state = {}, action) {
    switch (action.type) {
        case FETCH_REVIEWS:
            return {
                movie_id: action.payload.data[0].movie_id,
                rev_list: _.mapKeys(action.payload.data, 'id')
            };
        case CREATE_REVIEW:
            let reviews = {[action.payload.data.id]: action.payload.data};
            if (state.movie_id === action.payload.data.movie_id)
                reviews = {[action.payload.data.id]: action.payload.data, ...state.rev_list};
            return {
                movie_id: action.payload.data.movie_id,
                rev_list: reviews
            };
        default:
            return state;
    }
}
