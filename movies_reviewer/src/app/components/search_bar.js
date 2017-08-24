import React from 'react';


const SearchBar = (props) => {
    return (
        <input className="search-bar"
               placeholder="Search ..."
               onKeyPress={event => {if (event.which === 13) props.onSearchTermChange(event.target.value);}}/>
    );
};

export default SearchBar;
