import React from 'react';
import Book from './Book'
import PropTypes from 'prop-types'

function BookShelf(props){
    return(
        <div className="bookshelf">
            <h2 className="bookshelf-title">{ props.title }</h2>
            <div className="bookshelf-books">
                <ol className="books-grid">
                    {
                        props.books.map((book) => <Book key={ book.id } book={book} onShelfChange={ props.onShelfChange }/>)
                    }
                </ol>
            </div>
        </div>

    )}

BookShelf.PropTypes = {
    books: PropTypes.array,
    onShelfChange: PropTypes.func
};

export default BookShelf;