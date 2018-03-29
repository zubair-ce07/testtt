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
                <div className={'container'}>
                    {this.props.categories.map(function(category){
                        return <div key={category.path} className={'row'}>
                                <Link to={`/category/${category.name}`} >{category.name}</Link>
                            </div>;
                        })}

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





