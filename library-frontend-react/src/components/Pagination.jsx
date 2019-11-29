import React, { Component } from "react"

class Pagination extends Component {
  createPages = () => {
    const { current, pagesCount, setCurrentPage } = this.props
    let pages = []
    const itemClass = "page-item"

    for (let i = 1; i <= pagesCount; i++) {
      const navItemclass =
        i === parseInt(current) ? itemClass + " active" : itemClass
      pages.push(
        <li key={i} className={navItemclass}>
          <a className="page-link" href="#" onClick={() => setCurrentPage(i)}>
            {i}
          </a>
        </li>
      )
    }
    return pages
  }

  handlePageChange(pageNo) {
    const { setCurrentPage } = this.props
    setCurrentPage(pageNo)
  }

  render() {
    const { next, previous, pagesCount } = this.props

    const itemClass = "page-item"
    const disabled = " disabled"
    const nextClassName = next ? itemClass : itemClass + disabled
    const prevClassName = previous ? itemClass : itemClass + disabled

    return (
      <nav aria-label="Page navigation example">
        <ul className="pagination justify-content-end">
          <li className={prevClassName}>
            <a
              className="page-link"
              onClick={() => this.handlePageChange(previous)}
              href="#"
              tabIndex="-1"
            >
              Previous
            </a>
          </li>
          {this.createPages(pagesCount)}
          <li className={nextClassName}>
            <a
              className="page-link"
              onClick={() => this.handlePageChange(next)}
              href="#"
            >
              Next
            </a>
          </li>
        </ul>
      </nav>
    )
  }
}

export default Pagination
