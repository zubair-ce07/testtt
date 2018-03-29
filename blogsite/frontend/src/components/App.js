import React, {Component} from 'react';
import Categories from '../containers/Categories';
import Posts from '../containers/Posts';
import {connect} from 'react-redux';
import { Switch } from 'react-router';
import 'react-tabs/style/react-tabs.css';
import { Tab, Tabs, TabList, TabPanel} from 'react-tabs';
import {BrowserRouter as Router, Link, Route } from 'react-router-dom';
import Post from '../containers/Post';
import Category from '../containers/Category';

class App extends Component {

    render() {
        return (

            <Router>
                <div>

                    <Tabs  defaultIndex={window.location.pathname==='/'?0:1}>
                        <TabList>
                            <Tab><Link to='/'>Categories</Link></Tab>
                            <Tab><Link to='/posts'>Posts</Link></Tab>
                        </TabList>
                        <TabPanel/>
                        <TabPanel/>
                    </Tabs>


                    <hr />
                    <Switch>

                        <Route exact path='/' component={Categories} />
                        <Route path={`/category/:category`}  component={Category}/>
                        <Route path={'/posts/:post'} component={Post}/>
                        <Route path='/posts' component={Posts} />
                    </Switch>

                </div>
            </Router>

        )
    }
}
export default connect()(App);





