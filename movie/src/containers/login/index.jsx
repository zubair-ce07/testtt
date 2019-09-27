import {connect} from "react-redux";
import {LoginView} from "./login";
import {loginUser} from '../../actions/login';

const mapStateToProps = (state) => state;
const LoginContainer = connect(mapStateToProps, {loginUser})(LoginView);
export default LoginContainer;
