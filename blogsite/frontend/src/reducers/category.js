import * as types from '../actions/actionTypes';
import initialState from './initialState';


export default function categoryReducer(state =initialState.categories, action) {

    switch(action.type) {

        case types.LOAD_CATEGORY_PROGRESS: {
            return{
                ...state,
                isFetching:true
            }

        }
        case types.LOAD_CATEGORY_SUCCESS: {
            return{
                ...state,
                categories:action.data.categories,
                isFetching:false
            }

        }
        case types.LOAD_CATEGORY_FAILED: {
            return{
                ...state,
                categories:action.data.categories,
                isFetching:false
            }

        }
        case types.LOAD_CATEGORY_POST_SUCCESS: {
            return{
                ...state,
                posts:action.data,
                isFetching:false
            }

        }
        case types.LOAD_CATEGORY_POST_FAILED: {
            return{
                ...state,
                posts:
                action.data,
                isFetching:false
            }
        }

        default:
            return state;
    }
}
