import { GET_POST, CREATE_POST, UPDATE_POST, DELETE_POST } from './post.types'
import { CREATE_COMMENT, UPDATE_COMMENT, DELETE_COMMENT } from '../comment/comment.types'
import { fulfilled, pending } from 'helpers/api'

const initial = {
  posts: [],
  postLoading: 0,
  commentLoading: 0

}

function addUpdatePost (state, action) {
  const post = action.payload.data.data
  const posts = state.posts.filter(p => p.id !== post.id)
  posts.unshift(post)
  return { ...state, posts, postLoading: state.postLoading ? state.postLoading - 1 : 0 }
}

function deletePost (state, action) {
  const post = action.payload.data.data
  const posts = state.posts.filter(p => p.id !== Number(post.id))
  return { ...state, posts, postLoading: state.postLoading ? state.postLoading - 1 : 0 }
}

function addUpdateComment (state, action) {
  const comment = action.payload.data.data
  const posts = state.posts.map((p) => {
    if (p.id === comment.post) {
      p.comments = p.comments.filter(c => c.id !== Number(comment.id))
      p.comments.unshift(comment)
    }
    return p
  })
  return { ...state, posts, commentLoading: state.commentLoading ? state.commentLoading - 1 : 0 }
}

function deleteComment (state, action) {
  const comment = action.payload.data.data
  const posts = state.posts.map((p) => {
    if (p.id === comment.post) {
      p.comments = p.comments.filter(c => c.id !== Number(comment.id))
    }
    return p
  })
  return { ...state, posts, commentLoading: state.commentLoading ? state.commentLoading - 1 : 0 }
}

export default function (state = initial, action) {
  switch (action.type) {
    case pending(GET_POST):
      return { ...state, postLoading: state.postLoading + 1 }
    case fulfilled(GET_POST):
      return { ...state, posts: action.payload.data, postLoading: state.postLoading - 1 }

    case pending(CREATE_POST):
      return { ...state, postLoading: state.postLoading + 1 }
    case fulfilled(CREATE_POST):
      return addUpdatePost(state, action)

    case pending(UPDATE_POST):
      return { ...state, postLoading: state.postLoading + 1 }
    case fulfilled(UPDATE_POST):
      return addUpdatePost(state, action)

    case pending(DELETE_POST):
      return { ...state, postLoading: state.postLoading + 1 }
    case fulfilled(DELETE_POST):
      return deletePost(state, action)

    case pending(CREATE_COMMENT):
      return { ...state, commentLoading: state.commentLoading + 1 }
    case fulfilled(CREATE_COMMENT):
      return addUpdateComment(state, action)

    case pending(UPDATE_COMMENT):
      return { ...state, commentLoading: state.commentLoading + 1 }
    case fulfilled(UPDATE_COMMENT):
      return addUpdateComment(state, action)

    case pending(DELETE_COMMENT):
      return { ...state, commentLoading: state.commentLoading + 1 }
    case fulfilled(DELETE_COMMENT):
      return deleteComment(state, action)
    default:
      return state
  }
}
