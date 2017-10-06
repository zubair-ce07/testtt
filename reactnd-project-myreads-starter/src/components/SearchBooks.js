import React from 'react';
import * as BooksAPI from '../BooksAPI'
import {Link} from 'react-router-dom'
import Book from './Book.js'
import PropTypes from 'prop-types'


class SearchBooks extends React.Component{
    constructor(){
        super();
        this.state = {
            searchResults: []
        };
        this.searchBook = this.searchBook.bind(this);
    }

    searchBook(event){
        BooksAPI.search(event.target.value, 20).then(searchResults => {
            this.setState({searchResults})
        });
    }

    render() {
        return(
            <div className="search-books">
                <div className="search-books-bar">
                    <Link className="close-search" to="/">Close</Link>
                    <div className="search-books-input-wrapper">
                        <input type="text" placeholder="Search by title or author" onChange={ this.searchBook }/>
                    </div>
                </div>
                {this.state.searchResults.length > 0 &&
                <div className="search-books-results">
                    <ol className="books-grid">
                        {
                            this.state.searchResults.map((book) => <Book key={ book.id } book={ book }
                                                                         onShelfChange={ this.props.onShelfChange }/>)
                        }
                    </ol>
                </div>
                }
            </div>
        )
    }
}

SearchBooks.PropTypes = {
    onShelfChange: PropTypes.func
};

export default SearchBooks;