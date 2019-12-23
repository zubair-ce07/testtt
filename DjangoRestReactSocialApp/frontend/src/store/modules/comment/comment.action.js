import { CREATE_COMMENT, UPDATE_COMMENT, DELETE_COMMENT } from './comment.types'
import { newRequest } from 'helpers/api'

export function createComment (data) {
  const requestObject = {
    method: 'POST',
    url: '/social/comments/',
    data: data
  }
  return {
    type: CREATE_COMMENT,
    payload: newRequest(requestObject)
  }
}

export function updateComment (data, id) {
  const requestObject = {
    method: 'PUT',
    url: `/social/comments/${id}/`,
    data: data
  }
  return {
    type: UPDATE_COMMENT,
    payload: newRequest(requestObject)
  }
}

export function deleteComment (id) {
  const requestObject = {
    method: 'DELETE',
    url: `/social/comments/${id}/`
  }
  return {
    type: DELETE_COMMENT,
    payload: newRequest(requestObject)
  }
}
