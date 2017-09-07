import React from 'react'
import { connect } from 'react-redux'
import { searchWeather } from '../actions'

let SearchWeather = ({ dispatch }) => {
  let city

  return (
    <div>
      <form
        onSubmit={e => {
          e.preventDefault()
          if (!city.value.trim()) {
            return
          }
          dispatch(searchWeather(dispatch,city.value))
          city.value = ''
        }}
      >
        <input
          ref={node => {
            city = node
          }}
        />
        <button type="submit">
          Search
        </button>
      </form>
    </div>
  )
}
SearchWeather = connect()(SearchWeather)

export default SearchWeather