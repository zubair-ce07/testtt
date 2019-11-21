import axios from "axios"
import history from "../history"
import urls from "../urls.js"
import { baseApiUrl } from "../settings"

import { getCookieAuthToken, removeCookieAuthToken } from "../util/utils"

// import Notification from ".";
import responseCodes from "../contants/responseCodes"

let headers = { "Content-Type": "application/json" }

const requestConfig = {
  baseURL: baseApiUrl,
  headers: {
    "Content-Type": "application/json"
  }
}

const baseService = axios.create(requestConfig)

baseService.addAuthTokenToHeader = () => {
  const token = getCookieAuthToken()
  if (token) baseService.defaults.headers["Authorization"] = token
}

baseService.removeAuthToken = () => {
  removeCookieAuthToken()
  baseService.defaults.headers["Authorization"] = ""
  history.push(urls.signIn)
}

baseService.interceptors.response.use(config => {
  if (config.data.response_code === responseCodes.UNAUTHORIZED) {
    baseService.removeAuthToken()
    // Notification.error(config.data.error);
    return Promise.reject(config)
  } else {
    return config
  }
})

baseService.interceptors.request.use(
  config => {
    const token = getCookieAuthToken()
    if (token) config.headers["Authorization"] = token
    baseService.addAuthTokenToHeader()
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

export default baseService
