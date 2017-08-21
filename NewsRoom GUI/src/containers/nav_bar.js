import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Navbar, Nav, NavItem, NavDropdown, MenuItem } from 'react-bootstrap';
import { browserHistory } from 'react-router';
import { allCategories } from '../actions';
import { reactLocalStorage } from 'reactjs-localstorage';


class NavigationBar extends Component {
    constructor(props){
        super(props);
        const token = reactLocalStorage.get('token', "");
        this.obj = {log_logout: "", href_link: ""}
        if (token){
            this.obj.log_logout = "Logout"
            this.obj.href_link = ""
        }
        else{
            this.obj.log_logout = "Login"
            this.obj.href_link = "/login"
        }

    }

    componentDidMount() {
        this.props.allCategories();
    }
    renderDropdown(){
        console.log("Search Categories", this.props.categories);
        if (!this.props.categories) {
            return<li></li>
        }

        return this.props.categories.map(category => {
            return (
                <li key={category.name}><a href={`/news/categories/${category.name}`}>{category.name}</a></li>
            );
        })
    }

    clicked(event){
        if (this.obj.log_logout == "Logout"){
            reactLocalStorage.set('token', "");
        }
    }

    render(){
        console.log("render Categories", this.props.categories);
        const token = reactLocalStorage.get('token', "");
        
        return(
            <nav className="navbar navbar-inverse" role="navigation">
                <div className="navbar-header">
                    <button type="button" className="navbar-toggle" data-toggle="collapse" data-target=".navbar-ex1-collapse">
                        <span className="sr-only">Toggle navigation</span>
                        <span className="icon-bar"></span>
                        <span className="icon-bar"></span>
                        <span className="icon-bar"></span>
                    </button>
                    <div className="navbar-brand" href="">NewsRoom</div>
                </div>

                <div className="collapse navbar-collapse navbar-ex1-collapse">
                    <ul className="nav navbar-nav">
                        <li className="active"><a href="/news">Home</a></li>
                        <li className="dropdown">
                            <a href="#" className="dropdown-toggle" data-toggle="dropdown">Categories <b className="caret"></b></a>
                            <ul className="dropdown-menu">
                                {this.renderDropdown()}
                            </ul>
                        </li>
                    </ul>
                    <ul className="nav navbar-nav navbar-right">
                        <li><a onClick={this.clicked.bind(this)} href={this.obj.href_link}>{this.obj.log_logout}</a></li>
                    </ul>
                </div>
            </nav>
        );
    }
}

function mapStateToProps({ categories }) {
    return {
        categories
    };
}

export default connect(mapStateToProps, { allCategories })(NavigationBar);