import React from 'react'
import Book from './Book'


class BookShelf extends React.Component {
    render() {
        const books = this.props.books.map((book) => {
            return (
                <Book key={book.id} book={book} handleBookShelfChange={this.props.handleBookShelfChange}/>
            );
        });
        return (
            <div className="bookshelf">
                <h2 className="bookshelf-title">{this.props.title}</h2>
                <div className="bookshelf-books">
                    <ol className="books-grid">
                        {books}
                    </ol>
                </div>
            </div>
        );
    }
}


export default BookShelf;