import {connect} from "react-redux";
import {Home} from "./home";

const mapStateToProps = state => ({
    user: state.authReducer.user
});
const HomeContainer = connect(mapStateToProps)(Home);

export {HomeContainer};
