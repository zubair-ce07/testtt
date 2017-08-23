import _ from 'lodash';

import {FETCH_MOVIES} from '../actions/index';

const INITIAL_STATE = {};

export default function (state = INITIAL_STATE, action) {
    switch (action.type) {
        case FETCH_MOVIES:
            return _.mapKeys(action.payload.results, 'id');
        default:
            return state;
    }
}
