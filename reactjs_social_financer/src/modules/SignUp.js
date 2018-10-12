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
import Constants from '../utils/Constants'
import { Redirect } from "react-router-dom";
import Axios from 'axios';

const styles = theme => ({
  layout: {
    width: 'auto',
    display: 'block',
    marginLeft: theme.spacing.unit * 3,
    marginRight: theme.spacing.unit * 3,
    [theme.breakpoints.up(900 + theme.spacing.unit * 3 * 2)]: {
      width: 900,
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
    width: '90%', // Fix IE11 issue.
    marginTop: theme.spacing.unit,
  },
  submit: {
    marginTop: theme.spacing.unit * 3,
  },
  form_control: {
    minWidth: '45%',
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
  },
  address_field: {
    width: '93%',
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
  }

});

class SignUp extends React.Component {
  state = {
    authorized : false,
  }
  constructor(props){
    super(props);

    this.state = {
      input : {
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        phone_no: '',
        cnic_no: '',
        address: '',
        city: '',
        country: '',
        postal_code: '',
        display_picture: '',
      },
      error: '',
    };
  }

  handleSignUp = () => {
    console.log('here')
    const input = this.state.input;
    console.log(input)
    Axios.post(Constants.signupPOST,{
       body: input})
    .then(function (response) {
      console.log(response);
      this.setState({
        authorized: true
      })
    })
    .catch(function (error) {
    console.log(error);
    this.setState ({
      error: 'Please fill in all fields.'
    })
    });
  };

  handleInputChange = (newPartialInput) => {
    this.setState(state => ({
      ...state,
      input: {
        ...state.input,
        ...newPartialInput,
      }
    }))
  }

  componentDidMount() {
    document.title = 'Sign Up'
  }

  render() {
    const { classes } = this.props;
    const { input } = this.state

    if (this.state.authorized) {
      return <Redirect to='/'/>
    }

    return (
      <React.Fragment>
        <CssBaseline />
        <main className={classes.layout}>
          <Paper className={classes.paper}>
            <Avatar className={classes.avatar}>
              <LockIcon />
            </Avatar>
            <Typography variant="headline">Sign up</Typography>
            <form className={classes.form}>

              <FormControl margin="normal" required className={classes.form_control}>
                <InputLabel >First Name</InputLabel>
                <Input
                  id="firstName"
                  name="firstName"
                  autoComplete="firstname"
                  autoFocus
                  value={input.first_name}
                  onChange={e => this.handleInputChange({first_name: e.target.value})}
                />
              </FormControl>

              <FormControl margin="normal" required className={classes.form_control}>
                <InputLabel >Last Name</InputLabel>
                <Input
                  id="lastName"
                  name="lastName"
                  autoComplete="lastname"
                  value={input.last_name}
                  onChange={e => this.handleInputChange({last_name: e.target.value})}
                />
              </FormControl>

              <FormControl margin="normal" required className={classes.form_control}>
                <InputLabel >Phone Number</InputLabel>
                <Input
                  id="phoneNumber"
                  name="phoneNumber"
                  autoComplete="phoneNumber"
                  value={input.phone_no}
                  onChange={e => this.handleInputChange({phone_no: e.target.value})}
                />
              </FormControl>

              <FormControl margin="normal" required className={classes.form_control}>
                <InputLabel >Cnic no.</InputLabel>
                <Input
                  id="CnicNo"
                  name="CnicNo"
                  autoComplete="CnicNo"
                  value={input.cnic_no}
                  onChange={e => this.handleInputChange({cnic_no: e.target.value})}
                />
              </FormControl>

              <FormControl margin="normal" required className={classes.form_control}>
                <InputLabel htmlFor="email">Email Address</InputLabel>
                <Input id="email"
                  name="email"
                  autoComplete="email"
                  autoFocus
                  value={input.email}
                  onChange={e => this.handleInputChange({email: e.target.value})}
                />
              </FormControl>

              <FormControl margin="normal" required className={classes.form_control}>
                <InputLabel htmlFor="password">Password</InputLabel>
                <Input
                  name="password"
                  type="password"
                  id="password"
                  autoComplete="current-password"
                  value={input.password}
                  onChange={e => this.handleInputChange({password: e.target.value})}
                />
              </FormControl>

              <FormControl margin="normal" required fullWidth className={classes.address_field}>
                <InputLabel >Address</InputLabel>
                <Input
                  id="Address"
                  name="Address"
                  autoComplete="Address"
                  multiline
                  rows='2'
                  value={input.address}
                  onChange={e => this.handleInputChange({address: e.target.value})}
                />
              </FormControl>

              <FormControl margin="normal" required className={classes.form_control}>
                <InputLabel >City</InputLabel>
                <Input
                  id="City"
                  name="City"
                  autoComplete="City"
                  value={input.city}
                  onChange={e => this.handleInputChange({city: e.target.value})}
                />
              </FormControl>

              <FormControl margin="normal" required className={classes.form_control}>
                <InputLabel >Country</InputLabel>
                <Input
                  id="Country"
                  name="Country"
                  autoComplete="Country"
                  value={input.country}
                  onChange={e => this.handleInputChange({country: e.target.value})}
                />
              </FormControl>

              <FormControl margin="normal" required className={classes.form_control}>
                <InputLabel >Postal Code</InputLabel>
                <Input
                  id="Postal Code"
                  name="Postal Code"
                  autoComplete="Postal Code"
                  value={input.postal_code}
                  onChange={e => this.handleInputChange({postal_code: e.target.value})}
                />
              </FormControl>

              <FormControl required>
                <InputLabel >Display Picture</InputLabel>
                <Input
                  id="DisplayPicture"
                  name="DisplayPicture"
                  type="file"
                  value={input.display_picture}
                  onChange={e => this.handleInputChange({display_picture: e.target.value})}
                />
              </FormControl>

              <Button
                fullWidth
                color="primary"
                variant="raised"
                className={classes.submit}
                onClick={this.handleSignUp}
                >
                Sign up
              </Button>
            </form>
          </Paper>
        </main>
      </React.Fragment>
    );
  }
}

SignUp.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(SignUp);
