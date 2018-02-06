import React from 'react';
import Auth from '../services/auth.jsx';
import NavHeader from './Nav_header'
import Menu from './Menu'
import FreelancerMenu from '../freelancer/nav/Menu.jsx';


export default class Nav extends React.Component {

    menu(){
        let auth = new Auth()
        if(auth.isAuthenticated())
        {
            //TODO get user type
            //let type = "freelancer"   
            console.log("Rendering", "Freelancer");
            return (<FreelancerMenu />);

        }
        else
        {
            console.log("Rendering", "Default");
            return (<Menu />);
        }

    }

    render() {
        return (
            <nav className="navbar navbar-default" role="navigation">
                <div className="container">
                    <NavHeader />
                    {this.menu()}
                 <div className="clearfix"> </div>
                </div>
            </nav>
        );
    }
}
