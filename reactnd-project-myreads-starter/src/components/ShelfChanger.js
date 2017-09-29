import React from 'react';
import PropTypes from 'prop-types'

function ShelfChanger(props) {

    return (
        <div className="book-shelf-changer">
            <select value={ props.value } onChange={(e) => props.onShelfChange(e, props.book) }>
                <option value="none" disabled>Move to...</option>
                <option value="currentlyReading">Currently Reading</option>
                <option value="wantToRead">Want to Read</option>
                <option value="read">Read</option>
                <option value="none">None</option>
            </select>
        </div>
    );

}

ShelfChanger.PropTypes = {
    onShelfChange: PropTypes.func,
    value: PropTypes.string
};

export default ShelfChanger;
