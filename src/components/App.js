import React, {Component} from 'react';
import Search from '../containers/Search';
import Visualization from '../containers/Visualization';
import {connect} from 'react-redux';

class App extends Component {

    render() {
        return (
            <div className='container'>
                <Search/>
                {
                    this.props.weather.isFetching &&
                    <h2>{this.props.weather.message}</h2>
                }
                {
                    typeof this.props.weather.isFetching!=='undefined' &&
                    <Visualization/>
                }

                </div>

        )
    }
}
function mapStateToProps(state){
    return {
        weather: state.weather
    };
}
export default connect(mapStateToProps)(App);





