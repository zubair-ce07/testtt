import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Axios from 'axios';
import Constants from '../utils/Constants'

const styles = {
  root: {
    width: '100%',
    overflowX: 'auto',
  },
  table: {
    minWidth: 700,
  },
};

class FeedbackTable extends React.Component {
  state = {
    feedback : []
  }

  componentDidMount() {
    let token = 'Token ' + localStorage.getItem('accessToken')
    Axios.get(Constants.feedbackGET, {
      headers: {
        Authorization: token
      },
      params: {
        id: this.props.userId
      }
    })
    .then((response) => {
      console.log(response);
      this.setState({
        feedback: response.data
      })
    })
    .catch((error) => {
      console.log(error);
    });
  }

  render() {
    const { classes } = this.props;
    const { feedback } = this.state;
    return (
      <Paper className={classes.root}>
        <Table className={classes.table}>
          <TableHead>
            <TableRow>
              <TableCell>Received Feedback</TableCell>
              <TableCell>Rating /5</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {feedback.map(n => {
              return (
                <TableRow key={n.id}>
                  <TableCell component="th" scope="row">
                    {n.comments}
                  </TableCell>
                  <TableCell component="th" scope="row">
                    {n.star_rating}
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>

      </Paper>
    );
}
}

FeedbackTable.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(FeedbackTable);
