import _ from 'lodash';

import {FETCH_MOVIES} from '../actions/index';

export default function (state = {}, action) {
    switch (action.type) {
        case FETCH_MOVIES:
            return _.mapKeys(action.payload.results, 'id');
        default:
            return state;
    }
}
