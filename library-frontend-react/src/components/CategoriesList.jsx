import React, { Component } from "react"
import { getCategoriesList, setCurrentPage } from "actions/categoryActions"

import Loader from "components/Loader"
import Pagination from "components/Pagination"
import { connect } from "react-redux"
import { withRouter } from "react-router-dom"

class CategoriesList extends Component {
  componentDidMount() {
    this.props.getCategories(this.props.current)
  }

  componentDidUpdate(prevProps) {
    if (prevProps.current !== this.props.current) {
      this.props.getCategories(this.props.current)
    }
  }

  render() {
    const {
      categories,
      loading,
      current,
      previous,
      next,
      pagesCount,
      setCurrentPage
    } = this.props

    if (loading) return <Loader />
    if (categories.length < 1) return <h1>No Categories available</h1>

    return (
      <div className="container mx-auto mt-5">
        <h2 className="text-center">Available categories</h2>
        <div className="table-responsive-md">
          <table className="table table-bordered table-hover table-striped table-dark">
            <thead>
              <tr>
                <th scope="col">#</th>
                <th scope="col">Id</th>
                <th scope="col">Name </th>
              </tr>
            </thead>
            <tbody>
              {categories.map((category, index) => (
                <tr key={category.id}>
                  <th scope="row">{index + 1}</th>
                  <td>{category.id}</td>
                  <td style={{ maxWidth: "110px" }} className="text-truncate">
                    {category.name}
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
    categories: state.categories.categories,
    current: state.categories.currentPageNumber,
    previous: state.categories.previous,
    next: state.categories.next,
    pagesCount: state.categories.pagesCount,
    loading: state.categories.loading
  }
}

const mapDispatchToProps = dispatch => {
  return {
    getCategories: search => {
      dispatch(getCategoriesList(search))
    },

    setCurrentPage: pageNo => {
      dispatch(setCurrentPage(pageNo))
    }
  }
}
export default withRouter(
  connect(mapStateToProps, mapDispatchToProps)(CategoriesList)
)
