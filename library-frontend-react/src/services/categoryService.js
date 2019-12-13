import { doGet, onError } from "services/baseService.js"

import urls from "urls"

const categoryService = {
  getCategory: categoryId => {
    return doGet(`/category/${categoryId}`).catch(error => {
      onError(error)
    })
  },

  getCategories: (pageNo, searchQuery = null) => {
    return doGet(urls.categories, {
      params: {
        page: pageNo,
        search: searchQuery
      }
    })
  },

  getCategoriesData: () => {
    return doGet(urls.categoriesData)
  }
}

export default categoryService
