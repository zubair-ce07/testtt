import SearchBar from './Search';
import { connect } from 'react-redux';
import { search } from '../../actions';


function mapStateToProps(state) {
    return {
        weather: state.weatherList
    };
}

function mapDispatchToProps(dispatch) {
    return {
        searchMethod: (query) => dispatch(search(query))
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(SearchBar);
