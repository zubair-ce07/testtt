import { doGet, doPost } from "services/baseService"

import responseCodes from "constants/responseCodes"
import urls from "urls"

const authService = {
  login: data => {
    return doPost(urls.login, data)
  },

  logout: () => {
    return doGet(urls.logout)
  },

  signUpAuthor: data => {
    return doPost(urls.authorSignUp, data, responseCodes.CREATED)
  },

  signUpPublisher: data => {
    return doPost(urls.publisherSignUp, data, responseCodes.CREATED)
  }
}

export default authService
