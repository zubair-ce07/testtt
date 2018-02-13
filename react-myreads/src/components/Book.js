import React from 'react'
import BookShelfChanger from './BookSehlfChanger'


class Book extends React.Component {
    render() {
        const book = this.props.book;
        return (
            <div className="book">
                <div className="book-top">
                    <div className="book-cover" style={{
                        width: 128,
                        height: 193,
                        backgroundImage: "url('" + book.imageLinks.thumbnail + "')"
                    }}/>
                    <BookShelfChanger handleBookShelfChange={this.props.handleBookShelfChange} book={this.props.book}/>
                </div>
                <div className="book-title">{book.title}</div>
                <div className="book-authors">{book.authors}</div>
            </div>
        )
    }
}

export default Book;