import React from 'react';
import MiniProfile from '../components/MiniProfile'
import Dashboard from './Dashboard'
import Axios from 'axios';
import Constants from '../utils/Constants'
import { Redirect } from "react-router-dom";

class ConsumerHome extends React.Component {
  state = {
    title: this.props.title,
    user: {first_name:'', last_name:''},
    authorized: false,
  }

  handleResponse = (response) => {
    if (response.data[0] === undefined) {
      this.setState({
        title: 'No donor has paired with you yet.',
        user: {}
      })
    }
    else {
      this.setState({
        user: response.data[0]
      })
    }
  }

  componentWillMount() {
    if (localStorage.getItem('accessToken') !== undefined) {
      this.setState({
        authorized: true
      })
    }
  }

  componentDidMount() {
    let token = 'Token ' + localStorage.getItem('accessToken')
    Axios.get(Constants.myDonorGET , {
      headers: {
        Authorization: token
      }
    })
    .then((response) => {
      this.handleResponse(response)

    })
    .catch((error) => {
      console.log(error);
    });
  }

  render() {
    if (!this.state.authorized) {
      return <Redirect to='/'/>
    }
    let content = (
      <div>
        <MiniProfile userId={localStorage.getItem('userId')} user={this.state.user}/>
      </div>
    )
    return (
      <React.Fragment>
      <div>
        <Dashboard content={content} title={this.state.title}/>
      </div>
      </React.Fragment>
    );
  }
}


export default ConsumerHome
