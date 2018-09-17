import React from 'react';
import MiniProfile from '../components/MiniProfile'
import FeedbackTable from '../components/FeedbackTable';
import Dashboard from './Dashboard'
import Axios from 'axios';
import Constants from '../utils/Constants'
import { Redirect } from "react-router-dom";


class Profile extends React.Component {

  state = {
    title: this.props.title,
    user: {first_name:'', last_name:''},
    authorized: false,
  };

  componentWillMount() {
    if (localStorage.getItem('accessToken') !== null) {
      this.setState({
        authorized: true
      })
    }
  }

  componentDidMount() {
    let token = 'Token ' + localStorage.getItem('accessToken')
    Axios.get(Constants.myProfileGET , {
      headers: { Authorization: token }
    })
    .then((response) => {
      this.setState({ user: response.data[0] })
    })
    .catch((error) => {
      console.log(error);
    });
  }

  render() {
    console.log(localStorage.getItem('accessToken'))
    if (this.state.authorized === false) {
      return <Redirect to='/' />
    }

    let content = (<div>
                    <MiniProfile userId={localStorage.getItem('userId')} user={this.state.user} isMyProfile='true'/>
                    <FeedbackTable userId={localStorage.getItem('userId')}/>
                  </div>)
    return (
      <React.Fragment>
      <div>
        <Dashboard content={content} title={this.state.title}/>
      </div>
      </React.Fragment>
    );
  }
}

export default Profile
