import React, {Component} from 'react';


class SearchBar extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="centered">
                <input className="search-bar"
                       placeholder="Search ..."
                       onKeyPress={event => {if(event.which === 13) this.props.onSearchTermChange(event.target.value);}}
                />
            </div>
        );
    }
}

export default SearchBar;
