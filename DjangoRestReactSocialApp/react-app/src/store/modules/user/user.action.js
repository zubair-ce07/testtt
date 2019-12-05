import { LOGIN_USER, REGISTER_USER, CURRENT_USER, UPDATE_USER } from './user.types'
import { newRequest } from 'helpers/api'
import { toFormData } from 'helpers/common'

export function login (data) {
  const requestObject = {
    method: 'POST',
    url: '/auth/',
    data: data
  }
  return {
    type: LOGIN_USER,
    payload: newRequest(requestObject)
  }
}

export function register (data) {
  const requestObject = {
    method: 'POST',
    url: '/social/users',
    data: {
      user: data
    }
  }
  return {
    type: REGISTER_USER,
    payload: newRequest(requestObject)
  }
}

export function updateUser (data) {
  const requestObject = {
    method: 'PUT',
    url: '/social/users/change',
    data: toFormData(data)
  }
  return {
    type: UPDATE_USER,
    payload: newRequest(requestObject)
  }
}

export function getCurrentUser () {
  const requestObject = {
    method: 'GET',
    url: '/social/current_user'
  }
  return {
    type: CURRENT_USER,
    payload: newRequest(requestObject)
  }
}
