import React, {Component} from 'react'

class BooksList extends Component {
    shelf = [
        {
            name: `currentlyReading`,
            title: `Currently Reading`
        },
        {
            name: `wantToRead`,
            title: `Want to Read`
        },
        {
            name: `read`,
            title: `Read`
        },
    ]

    render() {
        const shelfs = this.shelfs
        const books = this.props.books

        return (
            <div className="list-books">
                <div className="list-books-title">
                    <h1>MyReads</h1>
                </div>
                <div className="list-books-content">
                    <div>
                        { shelfs.map((shelf, index) => (
                            <BookShelf
                                title={shelf.title}
                                key={index}
                                books={books.filter((book) => book.shelf === shelf.name)}
                            />
                        )) }
                    </div>
                </div>
            </div>
        )
    }
}

