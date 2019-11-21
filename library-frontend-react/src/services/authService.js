import baseService from "./baseService"
import urls from "../urls"

export const login = data => {
  return baseService.post(urls.login, data)
}

export const logout = () => {
  return baseService.get(urls.logout)
}

export const signUpAuthor = data => {
  return baseService.post("/accounts/signup/author/", data.formData)
}

export const signUpPublisher = data => {
  return baseService.post(urls.signUpPublisher, data)
}
