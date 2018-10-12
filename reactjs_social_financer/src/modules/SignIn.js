import React from 'react';
import PropTypes from 'prop-types';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import FormControl from '@material-ui/core/FormControl';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import LockIcon from '@material-ui/icons/LockOutlined';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import withStyles from '@material-ui/core/styles/withStyles';
import { Link, Redirect } from "react-router-dom";
import Axios from 'axios';
import Constants from '../utils/Constants'

const styles = theme => ({
  layout: {
    width: 'auto',
    display: 'block',
    marginLeft: theme.spacing.unit * 3,
    marginRight: theme.spacing.unit * 3,
    [theme.breakpoints.up(400 + theme.spacing.unit * 3 * 2)]: {
      width: 400,
      marginLeft: 'auto',
      marginRight: 'auto',
    },
  },
  paper: {
    marginTop: theme.spacing.unit * 8,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: `${theme.spacing.unit * 2}px ${theme.spacing.unit * 3}px ${theme.spacing.unit * 3}px`,
  },
  avatar: {
    margin: theme.spacing.unit,
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE11 issue.
    marginTop: theme.spacing.unit,
  },
  submit: {
    // backgroundColor: theme.palette.primary,
    marginTop: theme.spacing.unit * 3,
  },
  caption: {
    margin: theme.spacing.unit,
  }
});

class SignIn extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      input : {
        email: '',
        password: '',
      },
      error: '',
      redirect: false,
      role: '',
    };
  }

  handleSignIn = () => {
    console.log(Constants.loginPOST)
    Axios.post(Constants.loginPOST, {
      user : {
      username : this.state.input.email,
      password : this.state.input.password
  }})
  .then((response) => {
    console.log(response.data);
    response.data.user.token && localStorage.setItem('accessToken', response.data.user.token);
    response.data.user.role && localStorage.setItem('userRole', response.data.user.role);
    response.data.user.id && localStorage.setItem('userId', response.data.user.id);
    this.setState({
      role: response.data.user.role,
      redirect: true
    });
  })
  .catch((error) => {
    console.log(error);
    this.setState ({
      error: 'Username/Password does not match'
    })
  });
};

componentDidMount() {
  document.title = 'Sign In'
}

  handleInputChange = (newPartialInput) => {
    this.setState(state => ({
      ...state,
      input: {
        ...state.input,
        ...newPartialInput,
      }
    }))
  };

  render() {
    const { classes } = this.props;
    const { input } = this.state;
    const { redirect } = this.state;
    const { error } = this.state;
    // const { role } =

    if (redirect) {
      if (this.state.role === 'DN'){
      return <Redirect to="/unpaired-consumers" />
      }
      if (this.state.role === 'CN') {
        return <Redirect to="/my-donor" />
      }
      if (this.state.role === 'AD') {
        const redirectUrl = Constants.baseUrl + 'admin/'
        var win = window.open(redirectUrl, '_blank');
        win.focus();
      }
    }

  return (
    <React.Fragment>
      <CssBaseline />
      <main className={classes.layout}>
        <Paper className={classes.paper}>
          <Avatar className={classes.avatar}>
            <LockIcon />
          </Avatar>
          <Typography variant="headline">Sign in</Typography>
          <form className={classes.form}>
            <FormControl margin="normal" required fullWidth>
              <InputLabel htmlFor="email">Email Address</InputLabel>
              <Input id="email"
                name="email"
                autoComplete="email"
                autoFocus
                value={input.email}
                onChange={e => this.handleInputChange({email: e.target.value})}
              />
            </FormControl>
            <FormControl margin="normal" required fullWidth>
              <InputLabel htmlFor="password">Password</InputLabel>
              <Input name="password"
                type="password"
                id="password"
                autoComplete="current-password"
                value={input.password}
                onChange={e => this.handleInputChange({password: e.target.value})}
              />
            </FormControl>

            <Typography variant="caption" className="caption">{error}</Typography>
            <Button
              fullWidth
              variant="raised"
              color="primary"
              className={classes.submit}
              onClick={this.handleSignIn}
            >
              Sign in
            </Button>
            <Link to="/signup">
            <Button
              fullWidth
              >
              Sign up
            </Button>
            </Link>
          </form>
        </Paper>
      </main>
    </React.Fragment>
  );
}
}

SignIn.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(SignIn);
