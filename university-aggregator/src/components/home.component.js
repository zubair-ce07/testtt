import React, { Component } from 'react'
import axios from 'axios';
import { EndPoint } from '../config';

export class Home extends Component {
  state = {
    institutions: []
  }
  componentDidMount() {
    axios.get(EndPoint.institutions)
      .then(res => {
        const institutions = res.data;
        console.log('institutions', institutions);
        this.setState({ institutions });
      })
  }
  getPrograms = (event) => {
    const id = event.target.value 
    this.props.history.push(`institutions/${id}/programs/`)   
  }
    render() {
      return (
      <div>  
      <h1>Choose University</h1>
      <select className="form-control" onChange={(e) => this.getPrograms(e)} >
        <option>Choose University</option>
        {this.state.institutions.map(institute => <option value={institute.id} key={institute.id}>{institute.name}</option>)}
      </select>
      </div> 
        )
    }
}