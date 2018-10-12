import React from 'react';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import InputLabel from '@material-ui/core/InputLabel';
import Input from '@material-ui/core/Input';
import Constants from '../utils/Constants';
import Axios from 'axios';
import FormControl from '@material-ui/core/FormControl';
import { withStyles } from '@material-ui/core/styles';

const styles = theme => ({
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

class EditProfileDialog extends React.Component {
  state = {
    input: {
      first_name: '',
      last_name: '',
      phone_no: '',
      cnic_no: '',
      address: '',
      city: '',
      country: '',
      postal_code: '',
      display_picture: '',
      pk: '',
    },
    error: '',
  }

  handleUpdateProfile = () => {
    let token = 'Token ' + localStorage.getItem('accessToken')
    this.handleInputChange({pk: localStorage.getItem('userId')})
    var  input  = this.state.input
    console.log(input)

    Axios.put(Constants.myProfileGET + localStorage.getItem('userId'),
    {
      first_name: input.first_name,
      last_name: input.last_name,
      phone_no: input.phone_no,
      cnic_no: input.cnic_no,
      address: input.address,
      city: input.city,
      country: input.country,
      postal_code: input.postal_code,
      display_picture: input.display_picture,
      pk: input.pk,
      'categories': input.categories,
      'user': input.user,
      'role': input.role,
    },
    { headers: { Authorization: token }}
   )
    .then((response) => {
      console.log(response);
      this.props.handleClose()
      this.props.refreshParent()
    })
    .catch((error) => {
    console.log(error);
    this.setState ({
      error: 'A network error occured.'
    })
    });
  }

  handleInputChange = (newPartialInput) => {
    this.setState(state => ({
      ...state,
      input: {
        ...state.input,
        ...newPartialInput,
      },
    }))
  }

  componentWillReceiveProps(nextProps) {

    if (nextProps.user !== this.props.user) {
      this.setState({
        input: {...(nextProps.user)},
      })
    }
  }

  render() {
    const { classes } = this.props;
    const { input } = this.state;

    return (
      <Dialog
          open={this.props.open}
          onClose={this.props.handleClose}
          aria-labelledby="form-dialog-title"
        >
          <form className={classes.form}>
          <DialogTitle id="form-dialog-title">Edit Profile</DialogTitle>
          <DialogContent>
            <DialogContentText>
              Please edit your profile below.
            </DialogContentText>



              <FormControl margin="normal" required className={classes.form_control}>
                <InputLabel >First Name</InputLabel>
                <Input
                  id="firstName"
                  name="firstName"
                  autoComplete="firstname"
                  autoFocus
                  value={ input.first_name}
                  onChange={e => this.handleInputChange({first_name: e.target.value})}
                  disabled={true}
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
                  disabled={true}
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

              <FormControl margin="normal" required fullWidth className={classes.address_field}>
                <InputLabel >Address</InputLabel>
                <Input
                  id="Address"
                  name="Address"
                  autoComplete="Address"
                  multiline
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

              <FormControl required>
                <InputLabel ></InputLabel>
                <Input
                  id="DisplayPicture"
                  name="DisplayPicture"
                  type="file"
                  value={input.display_picture || ''}
                  onChange={e => this.handleInputChange({display_picture: e.target.value})}
                />
              </FormControl>

              {/* <InputLabel htmlFor="rating-native-helper">Categories </InputLabel>
              <NativeSelect
                value={this.state.star_rating}
                onChange={e => this.handleInputChange({star_rating: e.target.value})}
                input={<Input name="rating" id="rating-native-helper" />}
              >
                <option value="" />
                <option value={1}>1</option>
                <option value={2}>2</option>
                <option value={3}>3</option>
                <option value={4}>4</option>
                <option value={5}>5</option>
              </NativeSelect> */}

              <DialogContentText>
                {this.state.error}
              </DialogContentText>
            </DialogContent>
            <DialogActions>
              <Button onClick={this.props.handleClose} color="primary">
                Cancel
              </Button>
              <Button onClick={this.handleUpdateProfile} color="primary">
                Update
              </Button>
            </DialogActions>
            </form>



        </Dialog>
    );
  }
}

export default withStyles(styles)(EditProfileDialog);
