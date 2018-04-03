import React, {Component} from 'react';
import Categories from '../containers/Categories';
import Posts from '../containers/Posts';
import { Switch } from 'react-router';
import 'react-tabs/style/react-tabs.css';
import { Tab, Tabs, TabList, TabPanel} from 'react-tabs';
import {BrowserRouter as Router, Link, Route } from 'react-router-dom';
import Post from '../containers/Post';

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
                        <TabPanel><Route exact path='/' component={Categories} /></TabPanel>
                        <TabPanel>
                            <Switch>
                                <Route path={'/posts/:post'} component={Post}/>
                                <Route path='/posts' component={Posts} />
                            </Switch>
                        </TabPanel>
                    </Tabs>


                    <hr />


                </div>
            </Router>

        )
    }
}
export default App;





