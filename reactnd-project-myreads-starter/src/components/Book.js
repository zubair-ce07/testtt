import React from 'react';
import ShelfChanger from './ShelfChanger.js'
import PropTypes from 'prop-types'

function Book(props){
    const {book} = props;
    const image = 'url(' + book.imageLinks.thumbnail + ')';
    return(
        <div className="book">
            <div className="book-top">
                <div className="book-cover" style={{ width: 128, height: 174, backgroundImage: image } }></div>
                <ShelfChanger onShelfChange={ props.onShelfChange } book={ book } value={ book.shelf }/>
            </div>
            <div className="book-title">{ book.title }</div>
            <div className="book-authors">{ book.authors }</div>
        </div>
    )}

Book.PropTypes = {
  book: PropTypes.object
};

export default Book;