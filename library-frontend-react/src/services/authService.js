import baseService from "./baseService"
import urls from "../urls"

const authService = {
  login: data => {
    return baseService.post(urls.login, data)
  },

  logout: () => {
    return baseService.get(urls.logout)
  },

  signUpAuthor: data => {
    return baseService.post(urls.authorSignUp, data)
  },

  signUpPublisher: data => {
    return baseService.post(urls.publisherSignUp, data)
  }
}

export default authService
