import React, {Component} from 'react';
import Loader from '../containers/Loader';
import {connect} from 'react-redux';
import {Link} from 'react-router-dom'
import {loadCategory} from '../actions/category';
class Categories extends Component {

    componentDidMount(){

        if(!this.props.categories.length)this.props.loadCategory()
    }

    render() {
        return (
            <div className={'container'}>
                <Loader isFetching={this.props.isFetching} />

                {this.props.categories.map(function(category){
                    return <div key={category.path} className={'row'}>
                        <Link to={`/category/${category.name}`} >{category.name}</Link>
                    </div>;
                })}

            </div>
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





