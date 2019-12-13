import { Link, withRouter } from "react-router-dom"
import React, { Component } from "react"
import {
  authorsString,
  categoriesString,
  formatDate,
  publisherString
} from "utils"
import { getBooksList, setCurrentPage } from "actions/bookActions"

import Loader from "components/Loader"
import Pagination from "components/Pagination"
import { connect } from "react-redux"
import { isAdmin } from "utils"
import urls from "urls"

class BooksList extends Component {
  componentDidMount() {
    this.props.getBooks(this.props.current)
  }

  componentDidUpdate(prevProps) {
    if (prevProps.current !== this.props.current) {
      this.props.getBooks(this.props.current)
    }
  }

  render() {
    const {
      user,
      books,
      loading,
      current,
      previous,
      next,
      pagesCount,
      setCurrentPage
    } = this.props

    const admin = isAdmin(user)

    if (loading) return <Loader />
    if (books.length < 1) return <h1>No Books available</h1>

    return (
      <div className="container mx-auto mt-5">
        <h2 className="text-center">
          Available books{" "}
          {admin && (
            <span>
              <Link to={urls.bookNew}>New Book</Link>
            </span>
          )}
        </h2>
        <div className="table-responsive-md">
          <table className="table table-bordered table-hover table-striped table-dark">
            <thead>
              <tr>
                <th scope="col">#</th>
                <th scope="col">Id</th>
                <th scope="col">Title</th>
                <th scope="col">isbn</th>
                <th scope="col">Pages</th>
                <th scope="col">Date Published</th>
                <th scope="col">Categories</th>
                <th scope="col">Authors</th>
                <th scope="col">Publisher</th>
              </tr>
            </thead>
            <tbody>
              {books.map((book, index) => (
                <tr key={book.isbn}>
                  <th scope="row">{index + 1}</th>
                  <td>
                    <Link to={urls.book + book.id}>{book.id}</Link>
                  </td>
                  <td style={{ maxWidth: "110px" }} className="text-truncate">
                    {book.title}
                  </td>
                  <td>{book.isbn}</td>
                  <td>{book.pages}</td>
                  <td>{formatDate(book.date_published)}</td>
                  <td style={{ maxWidth: "110px" }} className="text-truncate">
                    {categoriesString(book.categories)}
                  </td>
                  <td style={{ maxWidth: "110px" }} className="text-truncate">
                    {authorsString(book.authors)}
                  </td>
                  <td>{publisherString(book.publisher)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <Pagination
          next={next}
          current={current}
          previous={previous}
          setCurrentPage={setCurrentPage}
          pagesCount={pagesCount}
        />
      </div>
    )
  }
}

const mapStateToProps = (state, _ownProps) => {
  return {
    user: state.auth.currentUser,
    books: state.books.books,
    current: state.books.currentPageNumber,
    previous: state.books.previous,
    next: state.books.next,
    pagesCount: state.books.pagesCount,
    loading: state.books.loading
  }
}

const mapDispatchToProps = dispatch => {
  return {
    getBooks: search => {
      dispatch(getBooksList(search))
    },

    setCurrentPage: pageNo => {
      dispatch(setCurrentPage(pageNo))
    }
  }
}
export default withRouter(
  connect(mapStateToProps, mapDispatchToProps)(BooksList)
)
