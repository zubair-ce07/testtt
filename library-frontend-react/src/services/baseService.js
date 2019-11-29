import { AUTHORIZATION } from "../contants/global"
import axios from "axios"
import { baseApiUrl } from "../settings"
import { getAuthTokenCookie } from "../util/utils"
import history from "../history"
import responseCodes from "../contants/responseCodes"
import urls from "../urls.js"

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

export default baseService
