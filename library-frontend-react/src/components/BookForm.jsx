import { CustomField, CustomSelect } from "components/CustomFormikFields"
import { Form, Formik } from "formik"
import React, { PureComponent } from "react"
import {
  clearBookData,
  createBook,
  getBookDetail,
  updateBookDetails
} from "actions/bookActions"

import ErrorDetails from "components/ErrorDetails"
import Loader from "components/Loader"
import { connect } from "react-redux"
import { getAuthorsDataList } from "actions/authorActions"
import { getCategoriesDataList } from "actions/categoryActions"
import { getPublishersDataList } from "actions/publisherActions"
import { mapBooktoFormValues } from "utils"
import { withRouter } from "react-router-dom"

class BookForm extends PureComponent {
  componentDidMount() {
    const {
      edit,
      match,
      getBook,
      clearFormData,
      getAuthors,
      getCategories,
      getPublishers
    } = this.props

    const bookId = match.params.bookId
    if (edit && bookId) {
      getBook(bookId)
    } else {
      clearFormData()
    }
    getAuthors()
    getCategories()
    getPublishers()
  }

  handleSubmit = (values, { setSubmitting }) => {
    const { edit, match, newBook, updateBook } = this.props
    const authors = values.authors.map(author => ({
      id: author.value
    }))
    const categories = values.categories.map(category => ({
      id: category.value
    }))
    const publisher = { id: values.publisher.value }

    values.authors = authors
    values.categories = categories
    values.publisher = publisher

    const bookId = match.params.bookId

    edit && bookId ? updateBook(bookId, values) : newBook(values)
    setSubmitting(false)
  }

  validate = values => {
    const errors = {}

    if (!values.title) {
      errors.title = "Title is required"
    }
    if (!values.isbn) {
      errors.isbn = "ISBN is required"
    }

    if (values.isbn && values.isbn.length !== 13) {
      errors.isbn = "ISBN must be 13 digits"
    }

    if (!values.authors || (values.authors && values.authors.length < 1)) {
      errors.authors = "Atleast 1 author is required"
    }
    if (
      !values.categories ||
      (values.categories && values.categories.length < 1)
    ) {
      errors.categories = "Atleast 1 category is required"
    }
    if (!values.publisher || !values.publisher.value) {
      errors.publisher = "Publisher is required"
    }

    return errors
  }

  render() {
    const {
      edit,
      authors,
      bookInitialValues,
      categories,
      publishers,
      errors,
      loading
    } = this.props

    if (loading) return <Loader />

    const formLabel = edit ? "Edit Book" : "New Book"

    return (
      <div className="container mt-5">
        <div id="book-form" className="card mx-auto bg-light border-dark p-5">
          <h1>{formLabel}</h1>
          <ErrorDetails errors={errors} />
          <Formik
            initialValues={bookInitialValues}
            validate={this.validate}
            onSubmit={this.handleSubmit}
            enableReinitialize={true}
          >
            {props => {
              return (
                <Form>
                  <CustomField
                    label="Book title"
                    name="title"
                    placeholder="Title"
                  />

                  <CustomField label="ISBN" name="isbn" placeholder="ISBN" />

                  <CustomField
                    label="Date Published"
                    name="date_published"
                    placeholder="Date of publication"
                    type="date"
                  />

                  <CustomField
                    label="No of pages"
                    name="pages"
                    placeholder="Pages"
                    type="number"
                  />

                  <CustomSelect
                    isMutli
                    value={props.values.authors}
                    name="authors"
                    options={authors}
                    placeholder="Select Authors"
                    label="Authors (select at least 1)"
                    onChange={props.setFieldValue}
                    onBlur={props.setFieldTouched}
                  />

                  <CustomSelect
                    value={props.values.publisher}
                    name="publisher"
                    options={publishers}
                    placeholder="Select publisher"
                    label="Publisher"
                    onChange={props.setFieldValue}
                    onBlur={props.setFieldTouched}
                  />

                  <CustomSelect
                    isMutli
                    value={props.values.categories}
                    name="categories"
                    options={categories}
                    placeholder="Select categories"
                    label="Categories (select at least 1)"
                    onChange={props.setFieldValue}
                    onBlur={props.setFieldTouched}
                  />

                  <button
                    type="submit"
                    className="btn btn-primary"
                    disabled={props.isSubmitting}
                  >
                    Submit
                  </button>
                </Form>
              )
            }}
          </Formik>
        </div>
      </div>
    )
  }
}

const mapStateToProps = (state, _ownProps) => {
  return {
    errors: state.books.error,
    authors: state.authors.authorsData.map(data => ({
      value: data.id,
      label: data.full_name
    })),
    categories: state.categories.categoriesData.map(data => ({
      value: data.id,
      label: data.name
    })),
    publishers: state.publishers.publishersData.map(data => ({
      value: data.id,
      label: data.company_name
    })),
    bookInitialValues: mapBooktoFormValues(state.books.book),
    loading:
      state.authors.loading ||
      state.books.loading ||
      state.categories.loading ||
      state.publishers.loading
  }
}

const mapDispatchToProps = dispatch => {
  return {
    newBook: formData => dispatch(createBook(formData)),
    getBook: bookId => dispatch(getBookDetail(bookId)),
    updateBook: (bookId, formData) =>
      dispatch(updateBookDetails(bookId, formData)),
    clearFormData: () => dispatch(clearBookData()),
    getAuthors: () => dispatch(getAuthorsDataList()),
    getCategories: () => dispatch(getCategoriesDataList()),
    getPublishers: () => dispatch(getPublishersDataList())
  }
}

export default withRouter(
  connect(mapStateToProps, mapDispatchToProps)(BookForm)
)
