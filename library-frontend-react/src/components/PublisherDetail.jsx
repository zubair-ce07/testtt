import React, { Component } from "react"

import Loader from "./Loader"
import { connect } from "react-redux"
import { getPublisherDetail } from "../actions/publisherActions"
import { withRouter } from "react-router-dom"

class PublisherDetail extends Component {
  componentDidMount = () => {
    const { match, getAuthor } = this.props
    getAuthor(match.params.publisherId)
  }

  handleDelete = (event, publisherId) => {
    event.preventDefault()
    let res = window.confirm("Are you sure, you want to delete the publisher")
    if (res) {
      this.props.onDelete(publisherId)
    } else {
      return false
    }
  }

  render() {
    const { publisher, loading } = this.props

    if (loading) return <Loader />

    return (
      <div id="publisher-detail-wrapper" className="container mt-5">
        <div className="row">
          <div className="card mx-auto bg-light border-dark text-center">
            <div className="card-header border-dark font-weight-bold text-center">
              {publisher.company_name}
            </div>
            <div className="card-body bg-light">
              <ul id="publisher-detail" className="list-group list-group-flush">
                <li className="list-group-item">
                  Email: <span>{publisher.email}</span>
                </li>
                <li className="list-group-item">
                  Phone: <span>{publisher.phone}</span>
                </li>
                <li className="list-group-item">
                  Website: <span>{publisher.website}</span>
                </li>
                <li className="list-group-item">
                  Address: <span>{publisher.address}</span>
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
    publisher: state.publishers.publisher,
    loading: state.publishers.loading
  }
}

const mapDispatchToProps = dispatch => {
  return {
    getAuthor: publisherId => dispatch(getPublisherDetail(publisherId))
  }
}

export default withRouter(
  connect(mapStateToProps, mapDispatchToProps)(PublisherDetail)
)
