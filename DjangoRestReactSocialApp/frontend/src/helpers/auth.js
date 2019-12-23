export function login (data) {
  localStorage.setItem('user', JSON.stringify(data.user))
  localStorage.setItem('token', data.token)
}

export function logout () {
  localStorage.removeItem('user')
  localStorage.removeItem('token')
}

export function getUser () {
  if (isLogin()) { return JSON.parse(localStorage.getItem('user')) }
}
export function getToken () {
  if (isLogin()) { return localStorage.getItem('token') }
}

export function isLogin () {
  const token = localStorage.getItem('token')
  return token
}
