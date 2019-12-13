import { Link, withRouter } from "react-router-dom"
import React, { Component } from "react"
import {
  authorsString,
  categoriesString,
  formatDate,
  isAdmin,
  publisherString
} from "utils"
import { deleteBook, getBookDetail } from "actions/bookActions"

import Loader from "components/Loader"
import { connect } from "react-redux"
import urls from "urls"

class BookDetail extends Component {
  componentDidMount = () => {
    const { match, getBook } = this.props
    getBook(match.params.bookId)
  }

  handleDelete = (event, bookId) => {
    event.preventDefault()
    let res = window.confirm("Are you sure, you want to delete the book")
    if (res) {
      this.props.onDelete(bookId)
    } else {
      return false
    }
  }

  render() {
    const { book, loading, user } = this.props

    if (loading) return <Loader />

    const admin = isAdmin(user)

    return (
      <div id="book-detail-wrapper" className="container mt-5">
        <div className="row">
          <div className="card mx-auto bg-light border-dark text-center">
            <div className="card-header border-dark font-weight-bold text-center">
              {book.title}
            </div>
            <div className="card-body bg-light">
              <ul id="book-detail" className="list-group list-group-flush">
                <li className="list-group-item">
                  ISBN: <span>{book.isbn}</span>
                </li>
                <li className="list-group-item">
                  Wriiten By: <span>{authorsString(book.authors)}</span>
                </li>
                <li className="list-group-item">
                  Publised By: <span>{publisherString(book.publisher)}</span>
                </li>
                <li className="list-group-item">
                  Pages: <span>{book.pages}</span>
                </li>
                <li className="list-group-item">
                  Date Published: <span>{formatDate(book.date_published)}</span>
                </li>
                <li className="list-group-item">
                  Catgories: <span>{categoriesString(book.categories)}</span>
                </li>
              </ul>
            </div>
            {admin && (
              <div className="card-footer bg-light">
                <Link
                  className="btn btn-warning card-link text-white"
                  to={urls.book + book.id + "/edit"}
                >
                  Edit{" "}
                  <span>
                    <i className="far fa-edit"></i>
                  </span>
                </Link>
                <Link
                  className="btn btn-danger card-link"
                  onClick={event => this.handleDelete(event, book.id)}
                  to={urls.books}
                >
                  Delete{" "}
                  <span>
                    <i className="far fa-trash-alt"></i>
                  </span>
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    )
  }
}

const mapStateToProps = (state, _ownProps) => {
  return {
    user: state.auth.currentUser,
    book: state.books.book,
    loading: state.books.loading
  }
}

const mapDispatchToProps = dispatch => {
  return {
    getBook: bookId => dispatch(getBookDetail(bookId)),
    onDelete: bookId => dispatch(deleteBook(bookId))
  }
}

export default withRouter(
  connect(mapStateToProps, mapDispatchToProps)(BookDetail)
)
