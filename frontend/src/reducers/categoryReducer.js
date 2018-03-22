
import * as types from '../actions/actionTypes';
import initialState from './initialState';
import _ from 'underscore'


export default function categoryReducer(state = initialState, action) {
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
                categories:
                action.data.categories
            }

        }
        case types.LOAD_POST_SUCCESS: {
            return{
                ...state,
                posts:action.data
            }


        }
        case types.LOAD_POST_FAILED: {
            return{
                ...state,
                allPosts:
                action.data
            }

        }
        case types.LOAD_POSTS_SUCCESS: {
        return{
            ...state,
            allPosts:action.data
        }


    }
        case types.LOAD_POSTS_FAILED: {
            return{
                ...state,
                posts:
                action.data
            }

        }

        case types.GET_POST_SUCCESS: {
            return{
                ...state,
                post:action.data,
                comments:action.comments

            }


        }
        case types.GET_POST_FAILED: {
            return{
                ...state,
                post:
                action.data,
                comments:action.comments
            }

        }

        case types.DELETE_COMMENT_SUCCESS: {
            return Object.assign({}, state, {

                comments:state.comments.map((comment) => {
                    if (comment.id === action.id) return action.comment
                    else return comment

                }),
            })



        }
        case types.DELETE_COMMENT_FAILED: {
            return{
                ...state,
                post:
                action.data,
                comments:action.comments
            }

        }

case types.ADD_COMMENT_SUCCESS: {
            return {
                ...state,
                comments:state.comments.concat(action.comment),
            }



        }
        case types.ADD_COMMENT_FAILED: {
            return{
                ...state
            }

        }
        case types.EDIT_COMMENT_SUCCESS: {
            return Object.assign({}, state, {

                comment:action.comment
            })



        }
        case types.EDIT_COMMENT_FAILED: {
            return{
                ...state
            }

        }


        default:
            return state;
    }
}
