
import * as types from '../actions/actionTypes';
import initialState from './initialState';
import _ from 'underscore'


export default function categoryReducer(state =initialState.categories, action) {
    console.log(state)
    console.log(action)
    switch(action.type) {


        case types.LOAD_CATEGORY_SUCCESS: {
            return{
                ...state,
                categories:action.data.categories
            }

        }
        case types.LOAD_CATEGORY_FAILED: {
            return{
                ...state,
                categories:action.data.categories
            }

        }
        case types.LOAD_CATEGORY_POST_SUCCESS: {
            return{
                ...state,
                posts:action.data
            }

        }
        case types.LOAD_CATEGORY_POST_FAILED: {
            return{
                ...state,
                posts:
                action.data
            }
        }

        default:
            return state;
    }
}
