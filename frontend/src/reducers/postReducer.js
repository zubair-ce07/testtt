
import * as types from '../actions/actionTypes';
import initialState from './initialState';
import _ from 'underscore'


export default function weatherReducer(state = initialState.posts, action) {
    switch(action.type) {
        case types.LOAD_POST_REQUEST: {

            return{
                ...state,
                isFetching:true,message:'Loading...'
            }

        }
        case types.LOAD_POST_SUCCESS: {
alert("in reducer")
            return{
                ...state,
                posts:action.posts
            }


        }
        case types.LOAD_POST_FAILED: {
            return{
                ...state,
                isFetching:true,message:action.posts.message
            }

        }

        default:
            return state;
    }
}
