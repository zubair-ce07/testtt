import {GET_NETWORK, LOADING_MORE, LOADED_MORE, FETCHING_NETWORK} from '../actions/action_types';


export default function (state = {users: [], isFetching: true, next: null}, action) {
    switch (action.type) {
        case FETCHING_NETWORK:
            return {users: [], isFetching: true, next: null};
        case GET_NETWORK:
            return {users: action.payload.data.results, isFetching: false, next: action.payload.data.next};
        case LOADING_MORE:
            return {users: state.users, isFetching: state.next === action.payload, next: state.next};
        case LOADED_MORE:
            if (state.next === action.payload.config.url)
                return {
                    users: state.users.concat(action.payload.data.results),
                    isFetching: false,
                    next: action.payload.data.next
                };
            return state;
        default:
            return state;
    }
}
