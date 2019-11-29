import React, { Component } from "react"
import { concatStrings, isAdmin } from "../util/utils"

import Loader from "./Loader"
import { connect } from "react-redux"
import { getAuthorDetail } from "../actions/authorActions"
import { withRouter } from "react-router-dom"

class AuthorDetail extends Component {
  componentDidMount = () => {
    const { match, getAuthor } = this.props
    getAuthor(match.params.authorId)
  }

  handleDelete = (event, authorId) => {
    event.preventDefault()
    let res = window.confirm("Are you sure, you want to delete the author")
    if (res) {
      this.props.onDelete(authorId)
    } else {
      return false
    }
  }

  render() {
    const { author, loading, user } = this.props

    if (loading) return <Loader />

    const admin = isAdmin(user)

    return (
      <div id="author-detail-wrapper" className="container mt-5">
        <div className="row">
          <div className="card mx-auto bg-light border-dark text-center">
            <div className="card-header border-dark font-weight-bold text-center">
              {concatStrings(author.first_name, author.last_name)}
            </div>
            <div className="card-body bg-light">
              <ul id="author-detail" className="list-group list-group-flush">
                <li className="list-group-item">
                  First Name: <span>{author.first_name}</span>
                </li>
                <li className="list-group-item">
                  Last Name: <span>{author.last_name}</span>
                </li>
                <li className="list-group-item">
                  Email: <span>{author.email}</span>
                </li>
                <li className="list-group-item">
                  Phone: <span>{author.phone}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

const mapStateToProps = (state, _ownProps) => {
  return {
    user: state.auth.currentUser,
    author: state.authors.author,
    loading: state.authors.loading
  }
}

const mapDispatchToProps = dispatch => {
  return {
    getAuthor: authorId => dispatch(getAuthorDetail(authorId))
  }
}

export default withRouter(
  connect(mapStateToProps, mapDispatchToProps)(AuthorDetail)
)
