import React from "react";
import * as BooksAPI from "./BooksAPI";
import "./App.css";
import SearchBooks from "./components/SearchBooks.js";
import ListBooks from "./components/ListBooks.js";
import {BrowserRouter, Route} from "react-router-dom";

class BooksApp extends React.Component {
    constructor()
    {
        super();
        this.state = {
            books: [],
            searchResults: []

        };
        this.changeShelf = this.changeShelf.bind(this);
    }


    componentDidMount(){
        BooksAPI.getAll().then(books => {
            this.setState({books});
        })
    }

    changeShelf(shelf, book){
        BooksAPI.update(book, shelf.target.value).then(BooksAPI.getAll().then(books => {
            this.setState({books});
            this.forceUpdate();
        }))
    }

    render() {
        return (
            <BrowserRouter>
                <div>
                    <Route exact path='/' component={() => <ListBooks onShelfChange={this.changeShelf} books={ this.state.books }/>} />
                    <Route path="/search" component={() => <SearchBooks onShelfChange={this.changeShelf}/>} />
                </div>
            </BrowserRouter>
        )
    }
}

export default BooksApp;
