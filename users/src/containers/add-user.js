import React from 'react';
import {connect} from 'react-redux';
import {addUser} from '../actions'

let AddUser = ({ dispatch }) => {
  let id , first, last, age, description;


  return (
    <div>
      <form
        onSubmit={e => {
          e.preventDefault();
          let u = {
                id: id.value,
                first: first.value,
                last: last.value,
                age: age.value,
                description: description.value,
                thumbnail: "http://i.imgur.com/7yUvePI.jpg"
            }
          dispatch(addUser(u))
        }}>
            <input
              ref={node => {
                id = node
              }}
              placeholder="id" /><br/>

              <input
              ref={node => {
                first = node
              }}
              placeholder="first"/><br/>

              <input
              ref={node => {
                last = node
              }}
              placeholder="last"/><br/>

              <input
              ref={node => {
                age = node
              }}
              placeholder="age"/><br/>

              <input
              ref={node => {
                description = node
              }}
              placeholder="description"/><br/>

              <button type="submit"> Add User </button>
      </form>
    </div>
  )
}
AddUser = connect()(AddUser)

export default AddUser
