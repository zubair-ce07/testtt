import React from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import NativeSelect from '@material-ui/core/NativeSelect';
import InputLabel from '@material-ui/core/InputLabel';
import Input from '@material-ui/core/Input';
import Constants from '../utils/Constants';
import Axios from 'axios';

class FeedbackDialog extends React.Component {
  state = {
    input: {
      star_rating: '',
      comments: ''
    },
    error: '',
  }

  handleSubmitFeedback = () => {
    let token = 'Token ' + localStorage.getItem('accessToken')
    var { input } = this.state
    input.id = this.props.userId
    console.log(input)
    Axios.post(Constants.feedbackPOST, {
      input,
     },{headers: {
       Authorization: token
     }}
     )
    .then((response) => {
      console.log(response);
      this.props.handleClose()
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

  render() {
    return (
      <Dialog
          open={this.props.open}
          onClose={this.props.handleClose}
          aria-labelledby="form-dialog-title"
        >
          <DialogTitle id="form-dialog-title">Submit Feedback</DialogTitle>
          <DialogContent>
            <DialogContentText>
              Please submit your feedback.
            </DialogContentText>
            <TextField
              autoFocus
              margin="dense"
              id="name"
              label="Comments"
              multiline={true}
              fullWidth
              value={this.state.comments}
              onChange={e => this.handleInputChange({comments : e.target.value})}
              rows='3'
            />
            <InputLabel htmlFor="rating-native-helper">Rating </InputLabel>
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
            </NativeSelect>
            <DialogContentText>
              {this.state.error}
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={this.props.handleClose} color="primary">
              Cancel
            </Button>
            <Button onClick={this.handleSubmitFeedback} color="primary">
              Submit
            </Button>
          </DialogActions>
        </Dialog>
    );
  }
}

export default FeedbackDialog
