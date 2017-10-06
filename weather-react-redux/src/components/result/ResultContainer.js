import Result from './Result';
import { connect } from 'react-redux';



function mapStateToProps(state) {
    return {
        weather: state.weatherList
    };
}

export default connect(mapStateToProps)(Result);
