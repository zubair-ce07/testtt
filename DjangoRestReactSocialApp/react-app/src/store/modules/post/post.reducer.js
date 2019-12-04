import { GET_POST, CREATE_POST, UPDATE_POST, DELETE_POST } from './post.types'
import { CREATE_COMMENT, UPDATE_COMMENT, DELETE_COMMENT } from '../comment/comment.types'
import { fulfilled } from 'helpers/api'

const initial = {
  posts: []
}

function addUpdatePost (state, action) {
  const post = action.payload.data.data
  const posts = state.posts.filter(p => p.id !== post.id)
  posts.unshift(post)
  return { ...state, posts }
}

function deletePost (state, action) {
  const post = action.payload.data.data
  const posts = state.posts.filter(p => p.id !== Number(post.id))
  return { ...state, posts }
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
  return { ...state, posts }
}

function deleteComment (state, action) {
  const comment = action.payload.data.data
  const posts = state.posts.map((p) => {
    if (p.id === comment.post) {
      p.comments = p.comments.filter(c => c.id !== Number(comment.id))
    }
    return p
  })
  return { ...state, posts }
}

export default function (state = initial, action) {
  switch (action.type) {
    case fulfilled(GET_POST):
      console.log(action.payload.data)
      return { ...state, posts: action.payload.data }
    case fulfilled(CREATE_POST):
      return addUpdatePost(state, action)
    case fulfilled(UPDATE_POST):
      return addUpdatePost(state, action)
    case fulfilled(DELETE_POST):
      return deletePost(state, action)

    case fulfilled(CREATE_COMMENT):
      return addUpdateComment(state, action)
    case fulfilled(UPDATE_COMMENT):
      return addUpdateComment(state, action)
    case fulfilled(DELETE_COMMENT):
      return deleteComment(state, action)
    default:
      return state
  }
}
