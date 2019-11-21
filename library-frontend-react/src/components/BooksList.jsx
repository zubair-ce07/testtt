import React, { Component } from "react"
import { connect } from "react-redux"

import { getBooksList } from "../actions/bookActions"

class BooksList extends Component {
  componentDidMount() {
    this.props.getBooks()
  }
  render() {
    return <h1>{JSON.stringify(this.props.books)}</h1>
  }
}

const mapStateToProps = (state, ownProps) => {
  return {
    books: state.books.books
  }
}

const mapDispatchToProps = dispatch => {
  return {
    getBooks: search => {
      dispatch(getBooksList(search))
    }
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(BooksList)
