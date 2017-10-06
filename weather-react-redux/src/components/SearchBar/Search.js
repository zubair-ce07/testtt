import React, { Component } from 'react';

class SearchBar extends Component {
    render() {
        return (
            <div>
                <input
                    type="text"
                    placeholder="Enter City Name"
                    ref={(input) => { this.textInput = input; }}
                />
                <input
                    type="button"
                    value="Search"
                    onClick={() => this.props.searchMethod(this.textInput.value)}
                />
            </div>

        )
    }
}

export default SearchBar;