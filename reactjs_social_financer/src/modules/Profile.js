import React from 'react';
import MiniProfile from '../components/MiniProfile'
import FeedbackTable from '../components/FeedbackTable';
import Dashboard from '../components/Dashboard'
import Axios from 'axios';
import Constants from '../utils/Constants'
import { Redirect } from "react-router-dom";
import EditProfileDialog from '../components/EditProfileDialog';


class Profile extends React.Component {

  state = {
    title: this.props.title,
    user: {first_name:'', last_name:''},
    authorized: false,
    isEditProfileDialogOpen: false,
  };

  handelEditProfileDialogClose = () => {
    this.setState({
      isEditProfileDialogOpen: false
    })
  }

  handleEditProfileDialogOpen = () => {
    console.log('Here')
    this.setState({
      isEditProfileDialogOpen: true
    })
  }

  setUser = (updatedUser) => {
    this.setState({
      user: updatedUser,
    })
  }

  getData = () => {
    let token = 'Token ' + localStorage.getItem('accessToken')
    Axios.get(Constants.myProfileGET + localStorage.getItem('userId') , {
      headers: { Authorization: token },
      params: { pk: localStorage.getItem('userId')}
    })
    .then((response) => {
      this.setState({ user: response.data })
    })
    .catch((error) => {
      console.log(error);
    });
  }

  componentWillMount() {
    if (localStorage.getItem('accessToken') !== null) {
      this.setState({
        authorized: true
      })
    }
  }

  componentDidMount() {
    document.title = 'My Profile'
    this.getData()
  }

  render() {
    console.log(localStorage.getItem('accessToken'))
    if (this.state.authorized === false) {
      return <Redirect to='/' />
    }

    let content = (<div>
                    <MiniProfile userId={localStorage.getItem('userId')} user={this.state.user} isMyProfile='true'/>
                    <FeedbackTable userId={localStorage.getItem('userId')} />
                    <EditProfileDialog userId={localStorage.getItem('userId')}
                      user={this.state.user}
                      open={this.state.isEditProfileDialogOpen}
                      handleClose={this.handelEditProfileDialogClose}
                      refreshParent={this.getData}
                    />
                  </div>
                )

    return (
      <React.Fragment>
      <div>
        <Dashboard content={content} title={this.state.title} editBadge={true} onEditClick={this.handleEditProfileDialogOpen}/>
      </div>
      </React.Fragment>
    );
  }
}

export default Profile
