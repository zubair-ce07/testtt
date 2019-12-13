import { Link, withRouter } from "react-router-dom"
import React, { Component } from "react"
import { getPublishersList, setCurrentPage } from "actions/publisherActions"

import Loader from "components/Loader"
import Pagination from "components/Pagination"
import { connect } from "react-redux"
import urls from "urls"

class PublishersList extends Component {
  componentDidMount() {
    this.props.getPublishers(this.props.current)
  }

  componentDidUpdate(prevProps) {
    if (prevProps.current !== this.props.current) {
      this.props.getPublishers(this.props.current)
    }
  }

  render() {
    const {
      publishers,
      loading,
      current,
      previous,
      next,
      pagesCount,
      setCurrentPage
    } = this.props

    if (loading) return <Loader />
    if (publishers.length < 1) return <h1>No Publishers available</h1>

    return (
      <div className="container mx-auto mt-5">
        <h2 className="text-center">Available publishers</h2>
        <div className="table-responsive-md">
          <table className="table table-bordered table-hover table-striped table-dark">
            <thead>
              <tr>
                <th scope="col">#</th>
                <th scope="col">Id</th>
                <th scope="col">Company Name</th>
                <th scope="col">Email</th>
                <th scope="col">Phone</th>
                <th scope="col">Website</th>
                <th scope="col">Address</th>
              </tr>
            </thead>
            <tbody>
              {publishers.map((publisher, index) => (
                <tr key={publisher.id}>
                  <th scope="row">{index + 1}</th>
                  <td>
                    <Link to={urls.publisher + publisher.id}>
                      {publisher.id}
                    </Link>
                  </td>
                  <td>{publisher.company_name}</td>
                  <td>{publisher.email}</td>
                  <td>{publisher.phone}</td>
                  <td>{publisher.website}</td>
                  <td style={{ maxWidth: "110px" }} className="text-truncate">
                    {publisher.address}
                  </td>
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
    publishers: state.publishers.publishers,
    current: state.publishers.currentPageNumber,
    previous: state.publishers.previous,
    next: state.publishers.next,
    pagesCount: state.publishers.pagesCount,
    loading: state.publishers.loading
  }
}

const mapDispatchToProps = dispatch => {
  return {
    getPublishers: search => {
      dispatch(getPublishersList(search))
    },

    setCurrentPage: pageNo => {
      dispatch(setCurrentPage(pageNo))
    }
  }
}
export default withRouter(
  connect(mapStateToProps, mapDispatchToProps)(PublishersList)
)
