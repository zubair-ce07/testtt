import React from 'react';
import PropTypes from 'prop-types';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import CssBaseline from '@material-ui/core/CssBaseline';
import Card from '@material-ui/core/Card';
import CardMedia from '@material-ui/core/CardMedia';
import { withStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import { Link } from "react-router-dom";


const styles = theme => ({
  root: {
    display: 'flex',
  },
  toolbar: {
    paddingRight: 24,
  },
  toolbarIcon: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: '0 8px',
    ...theme.mixins.toolbar,
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  appBarShift: {
    // width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  title: {
    flexGrow: 1,
    fontWeight: 'bold'
  },
  appBarSpacer: theme.mixins.toolbar,
  content: {
    flexGrow: 1,
    padding: theme.spacing.unit * 3,
    height: '100vh',
    overflow: 'auto',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  card: {
    width: '80%',
  },
  media: {
  },
  barbutton: {
    backgroundColor: theme.palette.common.white,
    margin: theme.spacing.unit,
    color: theme.palette.secondary,
    fontWeight: 'bold',
    '&:hover': {
      backgroundColor: theme.palette.secondary,
      color: theme.palette.common.white,
    },
  }

});

class Home extends React.Component {

  decideDashboard = () => {
    let role = localStorage.getItem('userRole')
    if (role === 'DN') {
      return '/unpaired-consumers'
    }
    else if (role === 'CN') {
      return '/my-donor'
    }
  }
  getBarButton = () => {
    const { classes } = this.props;
    let dashboardPath = this.decideDashboard()
    let barButton = localStorage.getItem('accessToken') ? (
      <Link to={dashboardPath}>
        <Button variant="contained"
          color="secondary"
          className={classes.barbutton}>
            Dashboard
        </Button>
      </Link>) :
    (
      <Link to='/signin'>
        <Button variant="contained" color="secondary" className={classes.barbutton}>
          Login
        </Button>
      </Link>
    );
    return barButton
  }

  componentDidMount() {
    document.title = 'Home'
  }
    render() {
      const { classes } = this.props;

      return (
        <React.Fragment>
          <CssBaseline />
          <div className={classes.root}>
            <AppBar
              position="absolute"
              className={classes.appBar}
            >
              <Toolbar className={classes.toolbar}>

                <Typography variant="title" color="inherit" noWrap className={classes.title}>
                  Social Financer
                </Typography>
                {this.getBarButton()}
              </Toolbar>
            </AppBar>

            <main className={classes.content}>
              <div className={classes.appBarSpacer} />
              <Typography variant="display1" gutterBottom>

              </Typography>
              {/* {content} */}
              <Card className={classes.card}>
                <CardMedia
                  className={classes.media}
                  component="img"
                  height="600"
                  image= {require('../assets/home_page_2.png')}
                  title="My Donor"
                />
              </Card>
            </main>
          </div>
        </React.Fragment>
      );
    }
}

Home.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Home);
