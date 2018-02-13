import React from 'react'
import Book from './Book'
import * as BooksAPI from '../api/BooksAPI'
import {Redirect} from 'react-router-dom';


class BooksSearch extends React.Component {
    constructor() {
        super();
        this.state = {
            closeSearch: false,
            books: []
        }
    }

    handleBooks(books) {
        this.setState({
            books: books
        });
    };

    keyPress(e) {
        if (e.keyCode === 13) {
            BooksAPI.search(e.target.value).then((books) => this.setState({
                books: books
            }));
        }
    }


    handleBookShelfChange(event, book) {
        BooksAPI.update(book, event.target.value).then(
            this.setState({
                closeSearch: true
            })
        );
    };

    render() {
        if (this.state.closeSearch)
            return <Redirect to="/"/>;

        const books = this.state.books.map((book) => {
            return (
                <Book key={book.id} book={book}
                      handleBookShelfChange={(event, book) => this.handleBookShelfChange(event, book)}
                />
            );
        });

        return (
            <div className="search-books">
                <div className="search-books-bar">
                    <a className="close-search" href="/#/">Close</a>
                    <div className="search-books-input-wrapper">
                        <input type="text" placeholder="Search by title or author"
                               onKeyDown={(e) => this.keyPress(e)}/>
                    </div>
                </div>
                <div className="search-books-results">
                    <ol className="books-grid">
                        {books}
                    </ol>
                </div>
            </div>
        );
    }
}

export default BooksSearch;