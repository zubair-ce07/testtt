import React, {Component} from 'react';
import Category from '../containers/Category';
import {connect} from 'react-redux';
import {BrowserRouter as Router,Link, Route} from 'react-router-dom'
import {loadCategory} from "../actions/category";
class Categories extends Component {

    componentDidMount(){
        this.props.dispatch(loadCategory())
    }

    render() {
        return (

            <Router>
                <div>
                    <ul>
                        {this.props.categories.map(function(category){

                            return <li key={category.path}>
                                <Link to={`/category/${category.name}`} >{category.name}</Link>
                            </li>;
                        })}
                    </ul>

                    <Route path={`/category/:category`}  component={Category}/>
                </div>
            </Router>
        )
    }
}
function mapStateToProps(state){
    console.log(state)
    return {
        categories: state.rootReducer.categories.categories
    };
}
export default connect(mapStateToProps)(Categories);





