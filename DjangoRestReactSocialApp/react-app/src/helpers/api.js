import axios from 'axios'
import { getToken, logout } from './auth'
import { _exists, msgAlert } from './common'

const API_URL = process.env.REACT_APP_API_URL

export async function newRequest ({ method, url, params, data, headers, hideError, auth }, server) {
  // debugger;
  console.log(process.env)
  url = API_URL + url
  const token = getToken()
  headers = { ...headers }
  if (token) { headers = { ...headers, Authorization: `Bearer ${token}` } }
  console.log(headers)

  const response = await axios({ method, url, headers, data, auth }).catch(({ response }) => {
    if (_exists(response, 'data.detail') && response.data.detail.includes('Signature')) {
      logout()
      window.location.href = '/login'
      msgAlert('failure', 'Token is Expired. Please log in')
      return response
    }
    if (_exists(response, 'data.non_field_errors')) {
      msgAlert('failure', response.data.non_field_errors[0])
      return response
    }

    throw response

    // return { data: [] }
  })
  return response
}

export function pending (type) {
  return `${type}_PENDING`
}

export function fulfilled (type) {
  return `${type}_FULFILLED`
}
