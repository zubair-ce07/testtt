import React from "react";
import BookShelf from './BookShelf.js'
import {Link} from 'react-router-dom'
import PropTypes from 'prop-types'


function ListBooks(props){
    return (
        <div className="list-books">
            <div className="list-books-title">
                <h1>MyReads</h1>
            </div>
            <div className="list-books-content">
                <div>
                    <BookShelf title="Currently Reading" onShelfChange={ props.onShelfChange } books={
                        props.books.filter((book) => book.shelf === "currentlyReading")
                    }
                    />
                    <BookShelf title="Want to Read" onShelfChange={ props.onShelfChange } books={
                        props.books.filter((book) => book.shelf === "wantToRead")

                    }
                    />
                    <BookShelf title="Read" onShelfChange={ props.onShelfChange } books={
                        props.books.filter((book) => book.shelf === "read")

                    }
                    />

                </div>
            </div>
            <div className="open-search">
                <Link to='/search'>Add a Book</Link>
            </div>
        </div>
    )
}

ListBooks.propTypes = {
    onShelfChange: PropTypes.func,
    books: PropTypes.array
};

export default ListBooks;