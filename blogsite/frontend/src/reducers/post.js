import * as types from '../actions/actionTypes';
import initialState from './initialState';
import _ from 'underscore'

export default function categoryReducer(state = initialState.postState, action) {

    switch(action.type) {
        case types.LOAD_CATEGORY_PROGRESS: {
            return{
                ...state,
                isFetching:true
            }

        }

        case types.LOAD_POSTS_SUCCESS: {
            return{
                ...state,
                allPosts:action.data,
                isFetching:false

            }
        }
        case types.LOAD_POSTS_FAILED: {
            return{
                ...state,
                posts: action.data,
                isFetching:false

            }

        }
        case types.GET_POST_SUCCESS: {
            return{
                ...state,
                post:action.data,
                comments:action.comments,
                isFetching:false


            }

        }
        case types.GET_POST_FAILED: {
            return{
                ...state,
                post:
                action.data,
                comments:action.comments,
                isFetching:false

            }

        }
        case types.CREATE_POST_SUCCESS: {
            return {
                ...state,
                post:{
                    id: Math.random().toString(36).slice(2),
                    timestamp: '',
                    title: 'Default Title',
                    body: '',
                    author: 'Haniya',
                    category: 'Redux'
                },
                createPost:true,
                editPost:false
            }
        }
        case types.CREATE_POST_FAILED: {
            return{
                ...state
            }

        }
        case types.ADD_POST_SUCCESS: {
            return {
                ...state,

                allPosts:state.allPosts.concat(action.post),
                post:{},
                createPost:false
            }
        }
        case types.ADD_POST_FAILED: {
            return{
                ...state
            }

        }
        case types.EDIT_POST_SUCCESS: {
            return {
                ...state,

                post:action.post,
                editPost:true,
                createPost:false
            }
        }
        case types.EDIT_POST_FAILED: {
            return{
                ...state
            }

        }
        case types.UPDATE_POST_SUCCESS: {
            return {
                ...state,

                allPosts:state.allPosts.map((post) => {
                    if (post.id === action.id) return action.post
                    else return post

                }),
                editPost:false
            }
        }
        case types.UPDATE_POST_FAILED: {
            return{
                ...state
            }

        }
        case types.DELETE_POST_SUCCESS: {
            return { ...state,
                    allPosts: [
                        ...state.allPosts.slice(0,_.findIndex(state.allPosts,{id:action.id})),
                        ...state.allPosts.slice(_.findIndex(state.allPosts,{id:action.id}) + 1)

                    ]
                };
            }
        case types.DELETE_POST_FAILED: {
            return{
                ...state
            }

        }
        case types.SORT_ALL_POSTS: {
            return {
                ...state,

                allPosts:state.allPosts.sort((obj1, obj2) => {
                    return obj1[action.sortBy] - obj2[action.sortBy];

                })
            }
        }

        ///COMMENTS RELATED TO SPECIFIC POST///////////

        case types.UPDATE_COMMENT_SUCCESS: {
            return {
                ...state,

                comments:state.comments.map((comment) => {
                    if (comment.id === action.id) return action.comment
                    else return comment

                }),
                editComment:false
            }
        }
        case types.UPDATE_COMMENT_FAILED: {
            return{
                ...state
            }

        }
        case types.DELETE_COMMENT_SUCCESS: {

            return { ...state,
                comments: [
                    ...state.comments.slice(0,_.findIndex(state.comments,{id:action.id})),
                    ...state.comments.slice(_.findIndex(state.comments,{id:action.id}) + 1)

                ]
            };


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
            return  {
                ...state,

                comments:state.comments.concat(action.comment),
                comment:{},
                createComment:false
            }

        }
        case types.ADD_COMMENT_FAILED: {
            return{
                ...state
            }

        }
        case types.EDIT_COMMENT_SUCCESS: {
            return {
                ...state,

                comment:action.comment,
                editComment:true
            }
        }
        case types.EDIT_COMMENT_FAILED: {
            return{
                ...state
            }

        }
        case types.CREATE_COMMENT_SUCCESS: {
            return  {
                ...state,
                comment:{
                    id: Math.random().toString(36).slice(2),
                    timestamp: '',
                    body: '',
                    author: 'Haniya',
                    parentId:action.parentId
                },
                createComment:true
            }

        }
        case types.CREATE_COMMENT_FAILED: {
            return{
                ...state
            }
        }
        default:
            return state;
    }
}
