import { Link, Redirect } from 'react-router-dom';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import React from 'react';

import PropTypes from 'prop-types';

import * as Actions from './actions.js'
import BannerCompact from '../banner/banner-compact';
import LoginForm from './login-form.jsx';
import Sidebar from '../sidebar/sidebar.jsx';

class LoginPage extends React.Component {
     static propTypes =  {
                          actions: PropTypes.object,
                          user: PropTypes.string
                        };
    constructor(props) {
    console.log("Form", "Login");
    super(props);
    this.onLogin = props.onLogin;
    // set the initial component state
    this.state = {
      errors: {},
      user: {
        name: '	',
        password: ''
      }
    };  

    this.processForm = this.processForm.bind(this);
    this.changeUser = this.changeUser.bind(this);
  }
  changeUser(event) {
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
    this.props.actions.requestAuthorization(this.state.user);
   
  }

    render() {

      if (this.props.user !== "") {
          return <Redirect to='/' />;
        }

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

function mapStateToProps(state) {
  console.log(state);
  return {
    user: state.login_reducer.token
  };
}

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(Actions, dispatch)
  };
}
export default connect(
  mapStateToProps,
  mapDispatchToProps
)(LoginPage);

