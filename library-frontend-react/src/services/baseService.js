import { AUTHORIZATION } from "constants/global"
import axios from "axios"
import { baseApiUrl } from "settings"
import { getAuthTokenCookie } from "utils"
import history from "@history"
import responseCodes from "constants/responseCodes"
import urls from "urls.js"

const requestConfig = {
  baseURL: baseApiUrl,
  headers: {
    "Content-Type": "application/json"
  }
}

const baseService = axios.create(requestConfig)

baseService.addAuthTokenToHeader = () => {
  const token = getAuthTokenCookie()
  if (token) baseService.defaults.headers[AUTHORIZATION] = `Token ${token}`
}

baseService.removeAuthToken = () => {
  baseService.defaults.headers[AUTHORIZATION] = ""
  history.push(urls.signIn)
}

baseService.interceptors.response.use(config => {
  if (config.data.response_code === responseCodes.UNAUTHORIZED) {
    baseService.removeAuthToken()
    return Promise.reject(config)
  } else {
    return config
  }
})

baseService.interceptors.request.use(
  config => {
    const token = getAuthTokenCookie()
    if (token) config.headers[AUTHORIZATION] = `Token ${token}`
    baseService.addAuthTokenToHeader()
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

const onSuccess = (response, success_code = responseCodes.OK) => {
  if (response.status !== success_code) {
    return Promise.reject(response)
  }
  return Promise.resolve(response)
}

export const onNotFoundError = data => {
  let response = data.response
  if (response && response.status === responseCodes.NOT_FOUND)
    history.replace(urls.notFound)
  Promise.reject(response)
}

export const doPost = (url, data, success_code) => {
  return baseService
    .post(url, data)
    .then(response => onSuccess(response, success_code))
}

export const doPut = (url, data) => {
  return baseService.put(url, data).then(response => onSuccess(response))
}

export const doGet = (url, data = null) => {
  return baseService
    .get(url, data)
    .then(response => onSuccess(response))
    .catch(error => onError(error))
}

export const doDelete = url => {
  return baseService
    .delete(url)
    .then(response => onSuccess(response, responseCodes.NO_CONTENT))
    .catch(error => onNotFoundError(error))
}

export default baseService
