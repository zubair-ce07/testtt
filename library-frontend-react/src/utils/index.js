import { ROLE, USER } from "constants/global"

import Cookies from "js-cookie"
import moment from "moment"

export const getAuthTokenCookie = () => {
  const userData = getUserCookie()
  return userData.token ? userData.token : null
}

export const setAuthTokenCookie = token => {
  let userData = getUserCookie()
  userData["token"] = token
  setUserCookie(userData)
}

export const removeUserCookie = () => {
  Cookies.remove(USER)
}

export const setUserCookie = data => {
  try {
    Cookies.set(USER, JSON.stringify(data))
    return true
  } catch (e) {
    return false
  }
}

export const getUserCookie = () => {
  const userData = Cookies.get(USER)
  let data = {}
  try {
    if (userData) {
      data = JSON.parse(userData)
    }
  } catch (e) {
    console.log("error: ", e)
  }
  if (!data["name"]) {
    if (data.first_name && data.role === ROLE.AUTHOR) {
      data["name"] = data.first_name
      delete data.first_name
    } else if (data.company_name && data.role === ROLE.PUBLISHER) {
      data["name"] = data.company_name
      delete data.company_name
    }
  }

  return data
}

export const checkAdminUser = () => {
  const userData = getUserCookie()
  return isAdmin(userData)
}

export const isAdmin = (user = {}) => {
  return Boolean(user.token && user.role === ROLE.ADMIN)
}

export const formatDate = (dateString, format = "DD MMM YYYY") => {
  return moment(dateString).format(format)
}

export const mapBooktoFormValues = book => {
  const {
    authors,
    categories,
    isbn,
    date_published,
    pages,
    publisher,
    title
  } = book

  let bookInitialvalues = {}
  bookInitialvalues["date_published"] = date_published
  bookInitialvalues["isbn"] = isbn
  bookInitialvalues["pages"] = pages
  bookInitialvalues["title"] = title

  if (authors) {
    bookInitialvalues["authors"] = authors.map(author =>
      createOption(
        author.id,
        `${author.first_name} ${author.last_name} `.trim()
      )
    )
  }

  if (categories) {
    bookInitialvalues["categories"] = categories.map(category =>
      createOption(category.id, category.name)
    )
  }

  if (publisher) {
    bookInitialvalues["publisher"] = createOption(
      publisher.id,
      publisher.company_name
    )
  }

  return bookInitialvalues
}

const createOption = (value, label) => ({
  value: value,
  label: label
})

export const authorsString = authors => {
  if (!authors) return "Not availble"

  const authorsStr = authors.map(author =>
    concatStrings(author.first_name, author.last_name)
  )
  return authorsStr.join(", ")
}

export const concatStrings = (first, second) => {
  let name = first
  if (second) return name.concat(" ", second)
  return name
}

export const categoriesString = categories => {
  if (!categories) return "Not availble"
  return categories.map(category => category.name).join(", ")
}

export const publisherString = publisher => {
  if (!publisher) return "Not availble"

  return publisher.company_name
}

export const getPageNumberFromUrl = url => {
  return url ? new URL(url).searchParams.get("page") || 1 : null
}

export const onErrorAction = (err, type) => {
  const response = err.response

  return {
    type: type,
    payload: response ? response.data : err
  }
}
