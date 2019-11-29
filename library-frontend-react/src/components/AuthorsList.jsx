import { Link, withRouter } from "react-router-dom"
import React, { Component } from "react"
import { getAuthorsList, setCurrentPage } from "../actions/authorActions"

import Loader from "./Loader"
import Pagination from "./Pagination"
import { connect } from "react-redux"
import urls from "../urls"

class AuthorsList extends Component {
  componentDidMount() {
    this.props.getAuthors(this.props.current)
  }

  componentDidUpdate(prevProps) {
    if (prevProps.current !== this.props.current) {
      this.props.getAuthors(this.props.current)
    }
  }

  render() {
    const {
      authors,
      loading,
      current,
      previous,
      next,
      pagesCount,
      setCurrentPage
    } = this.props

    if (loading) return <Loader />
    if (authors.length < 1) return <h1>No Authors available</h1>

    return (
      <div className="container mx-auto mt-5">
        <h2 className="text-center">Available authors</h2>
        <div className="table-responsive-md">
          <table className="table table-bordered table-hover table-striped table-dark">
            <thead>
              <tr>
                <th scope="col">#</th>
                <th scope="col">Id</th>
                <th scope="col">First Name</th>
                <th scope="col">Last Name</th>
                <th scope="col">Email</th>
                <th scope="col">Phone</th>
              </tr>
            </thead>
            <tbody>
              {authors.map((author, index) => (
                <tr key={author.id}>
                  <th scope="row">{index + 1}</th>
                  <td>
                    <Link to={urls.author + author.id}>{author.id}</Link>
                  </td>
                  <td style={{ maxWidth: "110px" }} className="text-truncate">
                    {author.first_name}
                  </td>
                  <td>{author.last_name}</td>
                  <td>{author.email}</td>
                  <td>{author.phone}</td>
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
    authors: state.authors.authors,
    current: state.authors.currentPageNumber,
    previous: state.authors.previous,
    next: state.authors.next,
    pagesCount: state.authors.pagesCount,
    loading: state.authors.loading
  }
}

const mapDispatchToProps = dispatch => {
  return {
    getAuthors: search => {
      dispatch(getAuthorsList(search))
    },

    setCurrentPage: pageNo => {
      dispatch(setCurrentPage(pageNo))
    }
  }
}
export default withRouter(
  connect(mapStateToProps, mapDispatchToProps)(AuthorsList)
)
