
import * as types from '../actions/actionTypes';
import initialState from './initialState';
import _ from 'underscore'


export default function categoryReducer(state = initialState, action) {
    console.log(state)
    console.log(action)
    switch(action.type) {

/*

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
        case types.CREATE_POST_SUCCESS: {
            return Object.assign({}, state, {

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
            })
        }
        case types.CREATE_POST_FAILED: {
            return{
                ...state
            }

        }
        case types.ADD_POST_SUCCESS: {
            return Object.assign({}, state, {

                allPosts:state.allPosts.concat(action.post),
                post:{},
                createPost:false
            })
            /!*return {
                ...state,
                comments:state.comments.concat(action.comment),
                comment:{}
            }*!/



        }
        case types.ADD_POST_FAILED: {
            return{
                ...state
            }

        }

        case types.INITIALIZE_POST_SUCCESS: {
            return Object.assign({}, state, {

                post:action.post,
                editPost:true,
                createPost:false
            })
        }
        case types.INITIALIZE_POST_FAILED: {
            return{
                ...state
            }

        }

        case types.EDIT_POST_SUCCESS: {
            return Object.assign({}, state, {

                allPosts:state.allPosts.map((post) => {
                    if (post.id === action.id) return action.post
                    else return post

                }),
                editPost:false
            })
        }
        case types.EDIT_POST_FAILED: {
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
            return Object.assign({}, state, {

                allPosts:state.allPosts.sort((obj1, obj2) => {
                    return obj1[action.sortBy] - obj2[action.sortBy];

                })
            })
        }










*/


        case types.UPDATE_COMMENT_SUCCESS: {
            return Object.assign({}, state, {

                comments:state.comments.map((comment) => {
                    if (comment.id === action.id) return action.comment
                    else return comment

                }),
                editComment:false
            })
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
            return Object.assign({}, state, {

                comments:state.comments.concat(action.comment),
                comment:{},
                createComment:false
            })

        }
        case types.ADD_COMMENT_FAILED: {
            return{
                ...state
            }

        }
        case types.EDIT_COMMENT_SUCCESS: {
            return Object.assign({}, state, {

                comment:action.comment,
                editComment:true
            })



        }
        case types.EDIT_COMMENT_FAILED: {
            return{
                ...state
            }

        }
        case types.CREATE_COMMENT_SUCCESS: {
            return Object.assign({}, state, {

                comment:{

                    id: Math.random().toString(36).slice(2),
                    timestamp: '',
                    body: '',
                    author: 'Haniya',
                    parentId:state.post.id
                },
                createComment:true
            })



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
