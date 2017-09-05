import React, {Component} from 'react';
import { browserHistory} from 'react-router';
import Logout from '../containers/Logout'


class Home extends Component {

    componentWillMount(){
        if (!localStorage.getItem('token')) {
           browserHistory.push('/');
        }
    }
     componentWillUpdate(){
        if (!localStorage.getItem('token')) {
            browserHistory.push('/');
        }

    }
    render(){
         let sideBarActiveClass = 'active-menu waves-effect waves-dark';
         let sideBarDeactiveClass = 'waves-effect waves-dark'
        let user = JSON.parse(localStorage.getItem("user"));
         if (!user){
            browserHistory.push('/');
             return <div></div>;
         }
        return (

        <div  id="container">
            <nav className="navbar navbar-default top-navbar">
                <div className="navbar-header">

                    <a className="navbar-brand waves-effect waves-dark" href="/home"><i className="large material-icons">track_changes</i> <strong>Mems Book</strong></a>

                </div>

                <ul className="nav navbar-top-links navbar-right">
                      <li><a className="dropdown-button waves-effect waves-dark" href={'/profile'+user.id} data-activates="dropdown1"><i className="fa fa-user fa-fw"></i> <b>{ user.first_name+' '+user.last_name}</b> </a></li>
                      <Logout />
                </ul>
            </nav>

            <nav className="navbar-default navbar-side" role="navigation">
                <div className="sidebar-collapse">
                    <ul className="nav" id="main-menu">
                        <li>
                            <a className={window.location.href.search('addmem') !==-1?sideBarActiveClass:sideBarDeactiveClass} href="/addmem"><i className="fa fa-dashboard"></i> Add New Mem</a>
                        </li>
                        <li>
                            <a href="/public" className={window.location.href.search('public') !==-1?sideBarActiveClass:sideBarDeactiveClass}><i className="fa fa-desktop"></i> Public Mems</a>
                        </li>
                        <li>
                            <a href="/activities" className={window.location.href.search('activities') !==-1?sideBarActiveClass:sideBarDeactiveClass}><i className="fa fa-bar-chart-o"></i> Your Activities</a>
                        </li>
                        <li>
                            <a href="/addcategory" className={window.location.href.search('addcategory') !==-1?sideBarActiveClass:sideBarDeactiveClass}><i className="fa fa-qrcode"></i> Add Category</a>
                        </li>
                    </ul>
                </div>
            </nav>
            <div id="page-wrapper" style={{paddingLeft:10, paddingTop:10}}>
                {this.props.children}

            </div>
    </div>

        );
    };
};
export default Home;