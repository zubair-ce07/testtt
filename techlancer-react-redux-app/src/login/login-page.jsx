import { Link } from 'react-router-dom';
import React from 'react';


import BannerCompact from '../banner/banner-compact';
import LoginForm from './login-form.jsx';
import Sidebar from '../sidebar/sidebar.jsx';

const LoginPage = () =>  {
        return (
        <div>
            <BannerCompact/>    
            <div className="container">
                <Sidebar />
                <div className="col-md-8 single_right">
                   <div className="login-form-section">
                                <div className="login-content">
                                    <LoginForm/>
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
export default LoginPage;
