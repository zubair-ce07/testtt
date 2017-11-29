import React from 'react'
import BookShelf from './BookShelf'
import * as BooksAPI from '../api/BooksAPI'

class DashBoard extends React.Component {
    constructor() {
        super();
        this.state = {
            showSearchPage: false,
            books: []
        };
    }

    getShelves() {
        const books = this.state.books.slice();
    };

    getBooks(shelfName) {
        const books = this.state.books.slice();
        return books.filter((book) => book.shelf === shelfName);
    };

    handleBooks(books) {
        this.setState({
            books: books
        });
    };

    componentDidMount() {
        BooksAPI.getAll().then((i) => this.handleBooks(i));
    };

    handleBookShelfChange(event, book) {
        BooksAPI.update(book, event.target.value);
        BooksAPI.getAll().then((i) => this.handleBooks(i));
    };

    render() {
        return (
            <div className="app">
                <div className="list-books">
                    <div className="list-books-title">
                        <h1>MyReads</h1>
                    </div>
                    <div className="list-books-content">
                        <div>
                            <BookShelf books={this.getBooks("currentlyReading")}
                                       title="Currently Reading"
                                       handleBookShelfChange={(event, book) => this.handleBookShelfChange(event, book)}/>
                            <BookShelf books={this.getBooks("wantToRead")}
                                       title="Want to Read"
                                       handleBookShelfChange={(event, book) => this.handleBookShelfChange(event, book)}/>
                            <BookShelf books={this.getBooks("read")}
                                       title="Read"
                                       handleBookShelfChange={(event, book) => this.handleBookShelfChange(event, book)}/>
                        </div>
                    </div>
                    <div className="open-search">
                        <a href="/#/search">Add a book</a>
                    </div>
                </div>
            </div>
        )
    }
}


export default DashBoard;