import React, {Component} from 'react';
import Categories from '../containers/Categories';
import Posts from '../containers/Posts';
import {connect} from 'react-redux';
import {
    BrowserRouter as Router,
    Link,
    Route // for later
} from 'react-router-dom'
import {loadCategory, loadPosts} from "../actions/category";
import Post from "../containers/Post";
class App extends Component {

    render() {
        return (

            <Router>
                <div>
                    <ul>
                        <li>
                            <Link to="/">Categories</Link>
                        </li>
                        <li>
                            <Link to="/posts">Posts</Link>
                        </li>
                        <li>
                            <Link to="/topics">Topics</Link>
                        </li>
                    </ul>

                    <hr />

                    <Route  path="/" component={Categories} />
                    <Route  path="/posts" component={Posts} />
                </div>
            </Router>

        )
    }
}

export default connect()(App);





