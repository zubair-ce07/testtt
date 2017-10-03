import React, {Component} from 'react';
import { connect } from 'react-redux';
import { logout } from '../../actions/auth'
import { LinkContainer } from 'react-router-bootstrap'
import { NavLink, withRouter } from 'react-router-dom'

class MainNav extends Component{
  render(){

    const {id, logoutClicked} = this.props
  	return(
  		<nav className="navbar navbar-default">
        <div className="container-fluid">
          <div className="navbar-header">
            <a className="navbar-brand" href="#">SocialNetwork</a>
          </div>
          <ul className="nav navbar-nav">
            <li>
              <NavLink exact to="/">
                Home
              </NavLink>
            </li>
            <li>
              <NavLink exact to={"/profile/"+id}>
                Profile
              </NavLink>
            </li>
          </ul>
          <ul className="nav navbar-nav navbar-right" style={{marginTop: "8px", marginRight: "auto" }} >
            <li>
              <LinkContainer to="/login">
                <button className="btn btn-danger" onClick={ () => logoutClicked() }>
                  <span className="glyphicon glyphicon-log-in">
                  </span>
                  Logout
                </button>
              </LinkContainer>
            </li>
          </ul>
        </div>
      </nav>
  	);
  }
}
const mapStateToProps = (state) => ({
  id: state.authReducer.id
})

const mapdispatchToProps = (dispatch) => ({
  logoutClicked: () => {
    dispatch(logout());
  }
})


export default withRouter(connect(
	mapStateToProps,
	mapdispatchToProps
)(MainNav))