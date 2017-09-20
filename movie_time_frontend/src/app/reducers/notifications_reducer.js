import _ from 'lodash';

import {FETCH_NOTIFICATIONS, DELETE_NOTIFICATIONS, RESPOND_TO_FOLLOW_REQUEST} from '../actions/action_types';


export default function (state = {moviesReleased: [], user_requests:[]}, action) {
    switch (action.type) {
        case FETCH_NOTIFICATIONS:
            const moviesReleased = [], user_requests = [];
            _.map(action.payload.data.results, notification => {
                if(notification.verb === 'Movie Released')
                    moviesReleased.push(notification);
                else
                    user_requests.push(notification);
            });
            return {moviesReleased, user_requests};
        case DELETE_NOTIFICATIONS:
            const newState = {user_requests: state.user_requests, moviesReleased: []};
            _.map(state.moviesReleased, notification => {
                if(notification.id !== action.payload.data.id)
                    newState.moviesReleased.push(notification);
            });
            return newState;
        case RESPOND_TO_FOLLOW_REQUEST:
            const updatedState = {user_requests: [], moviesReleased: state.moviesReleased};
            _.map(state.user_requests, notification => {
                if(notification.action_object.id === action.payload.data.id)
                    notification.action_object = action.payload.data;
                updatedState.user_requests.push(notification);
            });
            return updatedState;
        default:
            return state;
    }
}
