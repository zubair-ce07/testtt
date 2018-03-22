import React, {Component} from 'react';
import Category from '../containers/Category';
import Posts from '../containers/Posts';
import {connect} from 'react-redux';
import {
    BrowserRouter as Router,
    Link,
    Route // for later
} from 'react-router-dom'
import {loadCategory, loadPosts} from "../actions/category";
class Categories extends Component {

    componentDidMount(){
        this.props.dispatch(loadCategory())
    }

    render() {
        return (

            <Router>
                <div>
                    <h1>Categories</h1>
                    <ul>

                        {this.props.categories.map(function(category){
                            return <li key={category.path}>
                                <Link to={`/category/${category.name}`} >
                                    {category.name}
                                </Link>
                            </li>;
                        })}
                    </ul>
                    <hr />

                    <Route path={`/category/:category`}  component={Category}/>
                </div>
            </Router>
        )
    }
}
function mapStateToProps(state){
    console.log(state)
    return {
        posts: state.rootReducer.data.posts,
        categories: state.rootReducer.data.categories
    };
}
export default connect(mapStateToProps)(Categories);





