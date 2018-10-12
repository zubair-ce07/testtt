import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
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

class SimpleTable extends React.Component {
  state = {
    users: [],
  };

  fetchData = () => {
    let token = 'Token ' + localStorage.getItem('accessToken')
    Axios.get(this.props.getUrl, {
      headers: {
        Authorization: token
      }
    })
    .then((response) => {
      console.log(response);
      this.setState({
        users: response.data
      })
    })
    .catch((error) => {
      console.log(error);
    });
  }

  componentDidMount() {
    this.fetchData()
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.reRender !== this.props.reRender) {
      this.fetchData()
    }
  }

  render() {
    const { classes } = this.props;

    return (
      <Paper className={classes.root}>
        <Table className={classes.table}>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell >Categories</TableCell>
              <TableCell >Address</TableCell>
              <TableCell >View on maps</TableCell>
              <TableCell >Action</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {this.state.users.map(n => {
              return (
                <TableRow key={n.id}>
                  <TableCell component="th" scope="row">
                    {n.first_name + ' ' + n.last_name}
                  </TableCell>
                  <TableCell >{n.categories.join(', ')}</TableCell>
                  <TableCell >{n.address}</TableCell>
                  <TableCell ><a href={Constants.mapUrl + n.address.split(' ').join('+')}>View on maps</a></TableCell>
                  {this.props.shouldPairButtonShow ?
                    (
                      <TableCell>
                      <Button
                        color='primary'
                        variant='raised'
                        capitalized='false'
                        onClick={() => this.props.handlePairClick(n.id)}
                        >
                          Pair
                        </Button>
                      </TableCell>
                    )
                    :
                    (
                      <TableCell>
                    <Button
                      color='primary'
                      variant='raised'
                      capitalized='false'
                      onClick={() => this.props.handleFeedbackClick(n.id)}
                      >
                        Feedback
                      </Button>
                      <a>     </a>
                      <Button
                        color='primary'
                        variant='raised'
                        capitalized='false'
                        onClick={() => this.props.handleReportClick(n.id)}
                        >
                          Report
                        </Button>
                        </TableCell>
                    )}
                  {/* {this.props.actionButton} */}
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </Paper>
    );
  }
}
SimpleTable.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(SimpleTable);
