import baseService from "./baseService.js"
import urls from "../urls"

const categoryService = {
  getCategory: categoryId => {
    return baseService.get(`/category/${categoryId}`)
  },

  getCategories: (pageNo, searchQuery = null) => {
    return baseService.get(urls.categories, {
      params: {
        page: pageNo,
        search: searchQuery
      }
    })
  },

  getCategoriesData: () => {
    return baseService.get(urls.categoriesData)
  }
}

export default categoryService
