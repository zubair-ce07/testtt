import React from 'react'
import * as BooksAPI from './BooksAPI'
import './App.css'
import BookShelf from './components/BookShelf.js'
import Book from './components/Book.js'
import {HashRouter, Route, Link} from 'react-router-dom'

class BooksApp extends React.Component {
    constructor()
    {
        super();
        this.state = {
            books: [],
            searchResults: []

        };
        this.get_books = this.get_books.bind(this);
        this.changeShelf = this.changeShelf.bind(this);
        this.searchBook = this.searchBook.bind(this);
    }


    componentDidMount(){
        BooksAPI.getAll().then(books => {
            this.setState({books});
        })
    }

    get_books(shelf){
        let books = [];
        for(let i=0; i < this.state.books.length; i++){
            if(this.state.books[i].shelf === shelf){
                books.push(this.state.books[i]);
            }
        }
        return books;
    }

    changeShelf(shelf, book){
        BooksAPI.update(book, shelf.target.value).then(BooksAPI.getAll().then(books => {
            this.setState({books});
            this.forceUpdate();
        }))
    }

    searchBook(event){
        BooksAPI.search(event.target.value, 20).then(searchResults => {
            this.setState({searchResults})
        });
    }

    listBooks = () => (
        <div className="list-books">
            <div className="list-books-title">
                <h1>MyReads</h1>
            </div>
            <div className="list-books-content">
                <div>
                    <BookShelf title="Currently Reading" books={ this.get_books("currentlyReading") } onShelfChange={ this.changeShelf }/>
                    <BookShelf title="Want to Read" books={ this.get_books("wantToRead") } onShelfChange={ this.changeShelf }/>
                    <BookShelf title="Read" books={ this.get_books("read") } onShelfChange={ this.changeShelf } />

                </div>
            </div>
            <div className="open-search">
                <Link to='/search'>Add a Book</Link>
            </div>
        </div>
);

        searchBooks = () => (
        <div className="search-books">
            <div className="search-books-bar">
                <a className="close-search" onClick={() => this.setState({ showSearchPage: false })}>Close</a>
                <div className="search-books-input-wrapper">
                    <input type="text" placeholder="Search by title or author" onChange={ this.searchBook }/>
                </div>
            </div>
            {this.state.searchResults.length > 0 &&
            <div className="search-books-results">
                <ol className="books-grid">
                    {
                        this.state.searchResults.map((book) => <Book key={ book.id } book={ book }
                                                                     onShelfChange={ this.changeShelf }/>)
                    }
                </ol>
            </div>
            }
        </div>
        );

    render() {
        return (
            <HashRouter>
                <div>
                    <Route exact path='/' component={this.listBooks}/>
                    <Route path='/search' component={this.searchBooks}/>
                </div>
            </HashRouter>
    )
    }



}

export default BooksApp;
