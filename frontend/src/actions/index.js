
import * as actionType from './actionTypes';


export const loadCategoryRequest= ()=> ({
    type: actionType.LOAD_CATEGORY_REQUEST
})
export const loadCategorySuccess= (data)=> ({

    type: actionType.LOAD_CATEGORY_SUCCESS, data
})

export const loadCategoryFailed= (error)=> ({
    type: actionType.LOAD_CATEGORY_FAILED, error
})
export const getPostsRequest= ()=> ({
    type: actionType.LOAD_POST_REQUEST
})
export const getPostsSuccess= (data)=> ({

    type: actionType.LOAD_POST_SUCCESS, data
})

export const getPostsFailed= (error)=> ({
    type: actionType.LOAD_POST_FAILED, error
})
export const getAllPostsSuccess= (data)=> ({

    type: actionType.LOAD_POSTS_SUCCESS, data
})

export const getAllPostsFailed= (error)=> ({
    type: actionType.LOAD_POSTS_FAILED, error
})
export const getPostSuccess= (data, comments)=> ({

    type: actionType.GET_POST_SUCCESS, data, comments
})

export const getPostFailed= (error)=> ({
    type: actionType.GET_POST_FAILED, error
})
export const createPostSuccess= ()=> ({

    type: actionType.CREATE_POST_SUCCESS
})

export const createPostFailed= (error)=> ({
    type: actionType.CREATE_POST_FAILED, error
})

export const addPostSuccess= (post)=> ({

    type: actionType.ADD_POST_SUCCESS,post
})

export const addPostFailed= (error)=> ({
    type: actionType.ADD_POST_FAILED, error
})

export const initializePostSuccess= (post)=> ({

    type: actionType.INITIALIZE_POST_SUCCESS,post
})

export const initializePostFailed= (error)=> ({
    type: actionType.INITIALIZE_POST_FAILED, error
})

export const editPostSuccess= (post, id)=> ({

    type: actionType.EDIT_POST_SUCCESS,post, id
})

export const editPostFailed= (error)=> ({
    type: actionType.EDIT_POST_FAILED, error
})
export const deletePostSuccess= (post, id)=> ({

    type: actionType.DELETE_POST_SUCCESS,post, id
})

export const deletePostFailed= (error)=> ({
    type: actionType.DELETE_POST_FAILED, error
})
export const sortAllPosts= (sortBy)=> ({
    type: actionType.SORT_ALL_POSTS, sortBy
})


export const deleteCommentSuccess= (comment, id)=> ({

    type: actionType.DELETE_COMMENT_SUCCESS, comment, id
})

export const deleteCommentFailed= (error)=> ({
    type: actionType.DELETE_COMMENT_FAILED, error
})
export const addCommentSuccess= (comment)=> ({

    type: actionType.ADD_COMMENT_SUCCESS, comment
})

export const addCommentFailed= (error)=> ({
    type: actionType.ADD_COMMENT_FAILED, error
})
export const editCommentSuccess= (comment)=> ({

    type: actionType.EDIT_COMMENT_SUCCESS, comment
})

export const editCommentFailed= (error)=> ({
    type: actionType.EDIT_COMMENT_FAILED, error
})

export const updateCommentSuccess= (comment,id)=> ({

    type: actionType.UPDATE_COMMENT_SUCCESS, comment,id
})

export const updateCommentFailed= (error)=> ({
    type: actionType.UPDATE_COMMENT_FAILED, error
})
export const createCommentSuccess= (comment)=> ({

    type: actionType.CREATE_COMMENT_SUCCESS, comment
})
export const createCommentFailed= (error)=> ({

    type: actionType.CREATE_COMMENT_FAILED, error
})
