import React from 'react'
import { connect } from 'react-redux'
import { searchByCity } from '../actions'

let SearchByCity = ({ dispatch }) => {
    let city_name;

    return (
        <div>
            <form
                onSubmit={e => {
                    e.preventDefault();
                    if (!city_name.value.trim()) {
                        return
                    }
                    dispatch(searchByCity(city_name.value));
                    city_name.value = ''
                }}
            >
                <input ref={node => {city_name = node}}/>

                <button type="submit">Search City</button>
            </form>
        </div>
    )
};

const mapDispatchToProps = dispatch => {
    return {
        searchByCity: city_name => {
            dispatch(searchByCity(city_name))
        }
    }
};

SearchByCity = connect(mapDispatchToProps)(SearchByCity);

export default SearchByCity
