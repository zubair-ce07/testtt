import React from 'react';
import SignupForm from './signup-form';
import Registration from '../services/registration'

export default class Signup extends React.Component {

    constructor(props) {
    super(props);

    // set the initial component state
    this.state = {
      errors: {},
      user: {
        name: '',
        password: '',
        confirm_password: ''
      }
    };  

    this.processForm = this.processForm.bind(this);
    this.changeUser = this.changeUser.bind(this);
  }
  changeUser(event) {
    console.log(event);
    const field = event.target.name;
    const user = this.state.user;
    user[field] = event.target.value;
    
    this.setState({
      user
    });
  } 
  onRegister(result,errors){
    if(result)
      alert("User Registered");
    else
      alert(JSON.stringify(errors));
  }

  /**
   * Process the form.
   *
   * @param {object} event - the JavaScript event object
   */
  processForm(event) {
    // prevent default action. in this case, action is the form submission event
    event.preventDefault();

    console.log('name:', this.state.user.name);
    console.log('email:', this.state.user.password);
    console.log('password:', this.state.user.confirm_password);
    var registration  = new Registration();
    registration.registerFreelancer(this.state.user.name, this.state.user.password, this.onRegister);
  }


    render() {
        return (
            <div className="container">
                <div className="single">  
                   <div className="form-container">
                    <h2>Register Form</h2>
                    <SignupForm 
                        onSubmit={this.processForm}
                        onChange={this.changeUser}
                        errors={this.state.errors}
                        user={this.state.user}/>
                </div>
             </div>
            </div>
        );
    }
}
