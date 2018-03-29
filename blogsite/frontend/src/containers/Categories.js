import React, {Component} from 'react';
import Loader from '../containers/Loader';
import {connect} from 'react-redux';
import {BrowserRouter as Router,Link,Route} from 'react-router-dom'
import {loadCategory} from '../actions/category';
import Category from "./Category";
class Categories extends Component {

    componentDidMount(){

        if(!this.props.categories.length)this.props.loadCategory()
    }

    render() {
        return (
            <Router>
            <div className={'container'}>
                <Loader isFetching={this.props.isFetching} />

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
        categories: state.rootReducer.categories.categories,
        isFetching: state.rootReducer.categories.isFetching
    };
}
const mapDispatchToProps = (dispatch) => {
    return {
        loadCategory: () => {
            dispatch(loadCategory())
        }
    }
}
export default connect(mapStateToProps,mapDispatchToProps)(Categories);





