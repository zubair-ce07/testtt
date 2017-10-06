import React from 'react'
import { connect } from 'react-redux'
import { search } from '../actions'

let SearchBar = (props) => {
    let searchTerm;

    return (
        <div>
            <form
                onSubmit={e => {
                    e.preventDefault();
                    if (!searchTerm.value.trim()) {
                        return
                    }
                    props.searchVideo(searchTerm.value);
                    searchTerm.value = ''
                }}
            >
                <input ref={node => {searchTerm = node}}/>

                <button type="submit">Search</button>
            </form>
        </div>
    )
};

const mapDispatchToProps = dispatch => {
    return {
        searchVideo: searchTerm => {
            dispatch(search(searchTerm))
        }
    }
};

SearchBar = connect(null, mapDispatchToProps)(SearchBar);

export default SearchBar
