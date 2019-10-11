import React, { Component } from 'react'
import axios from 'axios';

export class Home extends Component {
  componentDidMount() {
    axios.get(`https://jsonplaceholder.typicode.com/users`)
      .then(res => {
        const institutions = res.data;
        // this.setState({ persons });
      })
  }
    render() {
      return (<h1>Home</h1>)
    }
}