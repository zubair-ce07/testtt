import { Link } from 'react-router-dom';
import React from 'react';
import BannerCompact from '../banner/banner-compact';
import LoginForm from './login-form.jsx';
import Sidebar from '../sidebar/sidebar.jsx';
import PropTypes from 'prop-types';
import Auth from '../services/auth.jsx'


export default class LoginPage extends React.Component {
    static propTypes = {onLogin: PropTypes.func.isRequired}

    constructor(props) {
    console.log("Form", "Login");
    super(props);
    this.onLogin = props.onLogin;
    // set the initial component state
    this.state = {
      errors: {},
      user: {
        name: '',
        password: ''
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

  /**
   * Process the form.
   *
   * @param {object} event - the JavaScript event object
   */
  processForm(event) {
    // prevent default action. in this case, action is the form submission event
    event.preventDefault();

    console.log('name:', this.state.user.name);
    console.log('email:', this.state.user.email);
    console.log('password:', this.state.user.password);
    let auth = new Auth();
    auth.authenticate(this.state.user.name, this.state.user.password, this.onLogin);
  }

    render() {
        return (
        <div>
            <BannerCompact/>    
            <div className="container">
                <Sidebar />
                <div className="col-md-8 single_right">
                   <div className="login-form-section">
                                <div className="login-content">
                                    <LoginForm
                                            onSubmit={this.processForm}
                                            onChange={this.changeUser}
                                            errors={this.state.errors}
                                            user={this.state.user}
                                        />
                                </div>
                            <div className="login-bottom">
                             <p>With your social media account</p>
                             <div className="social-icons">
                                <div className="button">
                                    <a className="tw" href="#"> <i className="fa fa-twitter tw2"> </i><span>Twitter</span>
                                    <div className="clearfix"> </div></a>
                                    <a className="fa" href="#"> <i className="fa fa-facebook tw2"> </i><span>Facebook</span>
                                    <div className="clearfix"> </div></a>
                                    <a className="go" href="#"><i className="fa fa-google-plus tw2"> </i><span>Google+</span>
                                    <div className="clearfix"> </div></a>
                                    <div className="clearfix"> </div>
                                </div>
                                <h4>Don,t have an Account? <Link to="/register"> Register Now!</Link></h4>
                             </div>
                           </div>
                                </div>
                         </div>
                        </div>
                        <div className="clearfix"> </div>
                    </div>
        );
    }
}
