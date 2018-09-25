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

class PairedConsumers extends React.Component {
  state = {
    open: true,
    authorized: false,
    reportDialogOpen: false,
    feedbackDialogOpen: false,
    dialogUserId: '',
  };

  // Dialog Actions
  handleFeedbackClick = (dialogUserId) => {
    console.log(dialogUserId)
    this.setState({
      feedbackDialogOpen: true,
      dialogUserId: dialogUserId,
    })
  }

  handleReportClick = (dialogUserId) => {
    this.setState({
      reportDialogOpen: true,
      dialogUserId: dialogUserId,
    })
  }

  handleCancelFeedback = () => {
    this.setState({
      feedbackDialogOpen: false
    })
  }

  handleCancelReport = () => {
    this.setState({
      reportDialogOpen: false
    })
  }

  componentWillMount() {
    if (localStorage.getItem('accessToken') !== null) {
      this.setState({
        authorized: true
      })
    }
  }

  componentDidMount() {
    document.title = 'Paired Consumers'
  }

  render() {
    if (this.state.authorized === false) {
      return <Redirect to='/' />
    }

    let dialogs = (
      <div>
        <FeedbackDialog open={this.state.feedbackDialogOpen}
          handleClose={this.handleCancelFeedback}
          userId={this.state.dialogUserId}/>
        <ReportDialog open={this.state.reportDialogOpen}
          handleClose={this.handleCancelReport}
          userId={this.state.dialogUserId }/>
        </div>
      )

    var content = (
      <div>
        <SimpleTable getUrl={Constants.pairedConsumerGET}
          handleFeedbackClick={this.handleFeedbackClick}
          handleReportClick={this.handleReportClick}
          shouldPairButtonShow={false}
        />
        {dialogs}
      </div>);

      return (
        <div>
        <Dashboard content={content}/>

        </div>
      );
  }

}

export default PairedConsumers;
