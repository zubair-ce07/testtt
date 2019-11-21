import Cookies from "js-cookie"

const AUTH = "Authorization"

export const getCookieAuthToken = () => {
  return Cookies.get(AUTH)
}

export const setCookieAuthToken = token => {
  Cookies.set(AUTH, `Token ${token}`)
}

export const removeCookieAuthToken = () => {
  Cookies.remove(AUTH)
}
