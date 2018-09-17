import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardHeader from '@material-ui/core/CardHeader';
import CssBaseline from '@material-ui/core/CssBaseline';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import CardMedia from '@material-ui/core/CardMedia';
import FeedbackDialog from './FeedbackDialog'
import ReportDialog from './ReportDialog'

const styles = theme => ({
  '@global': {
    body: {
      backgroundColor: theme.palette.common.white,
    },
  },
  layout: {
    width: 900,
    marginLeft: theme.spacing.unit*15,
    marginRight: theme.spacing.unit,
    justifyContent: 'center',
    alignItems: 'center'
  },
  cardHeader: {
    backgroundColor: theme.palette.grey[200],
  },
  cardContent: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'baseline',
    marginBottom: theme.spacing.unit * 2,
  },
  cardActions: {
    [theme.breakpoints.up('sm')]: {
      paddingBottom: theme.spacing.unit * 2,
    },
  },
  media: {
    objectFit: 'cover',
  },
});

class MiniProfile extends React.Component {
  state = {
    reportDialogOpen: false,
    feedbackDialogOpen: false
  }

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

  handle

  render() {
    const { classes } = this.props;
    const { user } = this.props;

    var cardActions = <div></div>
    if (this.props.isMyProfile === undefined) {
      cardActions = (
        <CardActions className={classes.cardActions}>
          <Button fullWidth variant='outlined' color="primary" onClick={this.handleFeedbackClick}>
            Post Feedback
          </Button>
          <Button fullWidth variant='outlined' color="primary" onClick={this.handleReportClick}>
            Report
          </Button>
        </CardActions>
      );
    }

    var card = <div></div>;
    if (user !== undefined) {
      card = (
        <Card>
          <CardMedia
            component="img"
            className={classes.media}
            height="280"
            image="http://chittagongit.com//images/profile-picture-icon/profile-picture-icon-29.jpg"
            title="My Donor"
          />
          <CardHeader
            title={user && user.first_name + ' ' + user.last_name}
            subheader= {user && user.city && user.city.toUpperCase()}
            titleTypographyProps={{ align: 'center' }}
            subheaderTypographyProps={{ align: 'center' }}
            action= {null}
            className={classes.cardHeader}
          />
          <CardContent>
            <div className={classes.cardContent}>
              <Typography variant="display2" color="textPrimary">
                {user && user.address}
              </Typography>
              <Typography variant="title" color="textSecondary">

              </Typography>
            </div>

              <Typography variant="title" align="center" key={1}>
                Phone no: {user && user.phone_no}
              </Typography>

          </CardContent>
          {cardActions}
        </Card>
      );
    }
    
    return (
    <React.Fragment>
      <CssBaseline />
      <main className={classes.layout}>

            <Grid item key='title' xs={12} >
              {card}
            </Grid>
      </main>
      <FeedbackDialog open={this.state.feedbackDialogOpen} handleClose={this.handleCancelFeedback} userId={user.id}/>
      <ReportDialog open={this.state.reportDialogOpen} handleClose={this.handleCancelReport} userId={user.id}/>
    </React.Fragment>
);
  }
}

MiniProfile.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(MiniProfile)
