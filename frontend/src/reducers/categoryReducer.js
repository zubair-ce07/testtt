
import * as types from '../actions/actionTypes';
import initialState from './initialState';
import _ from 'underscore'


export default function categoryReducer(state ={
    categories:[],
    posts:[]
}, action) {
    console.log(state)
    console.log(action)
    switch(action.type) {


        case types.LOAD_CATEGORY_REQUEST: {

            return{
                ...state,
                categories:action.data.categories
            }

        }
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

        default:
            return state;
    }
}
