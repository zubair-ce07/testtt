import React, {Component} from 'react';
import {withRouter} from "react-router-dom";

import NavigationBar from './navigation_bar/navigation_bar';
import SideNav from './navigation_bar/side_nav';

class App extends Component {
    constructor (props, context){
        super(props, context);
    }

    onFocusSearch() {
        this.props.history.push('/search/');
    }

    render() {
        return (
            <div>
                <NavigationBar/>
                <SideNav onFocusOnSearchBar={() => this.onFocusSearch()}/>
                {this.props.children}
            </div>
        );
    }
}

export default withRouter(App);
