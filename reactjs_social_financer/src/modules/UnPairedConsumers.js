import React from 'react';
import MiniProfile from '../components/MiniProfile'
import Dashboard from '../components/Dashboard'
import Axios from 'axios';
import Constants from '../utils/Constants'
import SimpleTable from '../components/SimpleTable'
import FeedbackDialog from '../components/FeedbackDialog'
import ReportDialog from '../components/ReportDialog'
import TableCell from '@material-ui/core/TableCell';
import Button from '@material-ui/core/Button';
import { Redirect } from "react-router-dom";

class UnPairedConsumers extends React.Component {
  state = {
    authorized: false,
    reRender: true,
    error: '',
  }
  // Dialog Actions
  handlePairClick = (userId) => {
    console.log(userId)

    let token = 'Token ' + localStorage.getItem('accessToken')
    Axios.post(Constants.pairUserPOST + userId, {
      pair_id : userId,
     },{headers: {
       Authorization: token
     }}
     )
    .then((response) => {
      console.log(response);
      this.setState({
        reRender: !this.state.reRender
      })
    })
    .catch((error) => {
    console.log(error);
    this.setState ({
      error: 'A network error occured.'
    })
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
    document.title = 'Unpaired Consumers'
  }

  render() {
    if (this.state.authorized === false) {
      return <Redirect to='/' />
    }

    var content = (
      <div>
        <SimpleTable getUrl={Constants.unpairedConsumersGET}
          shouldPairButtonShow={true}
          handlePairClick={this.handlePairClick}
          reRender={this.state.reRender}
        />
      </div>);

      return (
        <Dashboard content={content}/>
      );
  }

}

export default UnPairedConsumers;
