import React from 'react';
import MiniProfile from '../components/MiniProfile'
import Dashboard from '../components/Dashboard'
import Axios from 'axios';
import Constants from '../utils/Constants'
import FeedbackDialog from '../components/FeedbackDialog'
import ReportDialog from '../components/ReportDialog'
import CardActions from '@material-ui/core/CardActions';
import Button from '@material-ui/core/Button';
import { Redirect } from "react-router-dom";
import { withStyles } from '@material-ui/core/styles';

const styles = theme => ({
  cardActions: {
    [theme.breakpoints.up('sm')]: {
      paddingBottom: theme.spacing.unit * 2,
    },
  },
});


class ConsumerHome extends React.Component {
  state = {
    title: this.props.title,
    user: {first_name:'', last_name:'', id:'',},
    authorized: false,
    reportDialogOpen: false,
    feedbackDialogOpen: false,
  }

  // Dialog Actions
  handleFeedbackClick = () => {
    this.setState({
      feedbackDialogOpen: true
    })
  }

  handleReportClick = () => {
    this.setState({
      reportDialogOpen: true
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

  // Server Actions
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

  // Lifecycle
  componentWillMount() {
    if (localStorage.getItem('accessToken') !== undefined) {
      this.setState({
        authorized: true
      })
    }
  }
  componentDidMount() {
    document.title = 'My Donor'
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
    const { classes } = this.props;

    if (!this.state.authorized) {
      return <Redirect to='/'/>
    }

    let cardActions = (
      <CardActions className={classes.cardActions}>
        <Button fullWidth variant='outlined' color="primary" onClick={this.handleFeedbackClick}>
          Post Feedback
        </Button>
        <Button fullWidth variant='outlined' color="primary" onClick={this.handleReportClick}>
          Report
        </Button>
      </CardActions>
    );

    let dialogs = (
      <div>
        <FeedbackDialog open={this.state.feedbackDialogOpen}
          handleClose={this.handleCancelFeedback}
          userId={this.state.user.id}/>
        <ReportDialog open={this.state.reportDialogOpen}
          handleClose={this.handleCancelReport}
          userId={this.state.user.id}/>
        </div>
      )

        let content = (
          <div>
            <MiniProfile userId={localStorage.getItem('userId')}
              user={this.state.user}
              cardActions={cardActions}
            />
          </div>
        )

    return (
      <React.Fragment>
      <div>
        <Dashboard content={content}
          title={this.state.title}
        />
        {dialogs}
      </div>
      </React.Fragment>
    );
  }
}

export default withStyles(styles)(ConsumerHome);
