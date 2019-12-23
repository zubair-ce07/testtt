import { GET_POST, CREATE_POST, UPDATE_POST, DELETE_POST } from './post.types'
import { newRequest } from 'helpers/api'
import { toFormData } from 'helpers/common'

export function getPosts () {
  const requestObject = {
    method: 'GET',
    url: '/social/posts/'
  }
  return {
    type: GET_POST,
    payload: newRequest(requestObject)
  }
}

export function createPost (data) {
  const requestObject = {
    method: 'POST',
    url: '/social/posts/',
    data: toFormData(data)
  }
  return {
    type: CREATE_POST,
    payload: newRequest(requestObject)
  }
}

export function updatePost (data, id) {
  delete data.comments
  data.author = data.author.id

  if (typeof data.image === 'string') { delete data.image }
  const requestObject = {
    method: 'PUT',
    url: `/social/posts/${id}/`,
    data: toFormData(data)
  }
  return {
    type: UPDATE_POST,
    payload: newRequest(requestObject)
  }
}

export function deletePost (id) {
  const requestObject = {
    method: 'DELETE',
    url: `/social/posts/${id}/`
  }
  return {
    type: DELETE_POST,
    payload: newRequest(requestObject)
  }
}
