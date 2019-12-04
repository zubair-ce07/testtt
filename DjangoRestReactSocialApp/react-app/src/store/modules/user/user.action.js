import { LOGIN_USER, REGISTER_USER, CURRENT_USER } from './user.types'
import { newRequest } from 'helpers/api'

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
    url: '/register',
    data: {
      user: data
    }
  }
  return {
    type: REGISTER_USER,
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
