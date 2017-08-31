import React from "react";
import {Nav, Navbar, NavItem} from "react-bootstrap";
import SearchInput from 'react-search-input'
import {Link, withRouter} from "react-router-dom";
import {filters, setSearchText, setUser, setVisibilityFilter} from "../actions/index";
import {connect} from "react-redux";

const event = {
    LOGIN: 1,
    ADD_NEWS: 2,
    LOGOUT: 2.3,
};

let Header = (props) => {

    const searchBar = props.displaySearchBar ? (
        <NavItem>
            <SearchInput className="search-input"
                         placeholder="Search News"
                         onChange={props.handleSearchBar}/>
        </NavItem>
    ) : null;

    const authOrNonAuthNav = localStorage.authToken ? (
            <Nav pullRight onSelect={props.handleNavBarSelect}>
                {searchBar}
                <NavItem>{props.user.username}</NavItem>
                <NavItem eventKey={event.ADD_NEWS}>Add News</NavItem>
                <NavItem eventKey={event.LOGOUT}>Logout</NavItem>
            </Nav>
        ) :
        <Nav pullRight onSelect={props.handleNavBarSelect}>
            {searchBar}
            <NavItem eventKey={event.LOGIN}>LOGIN</NavItem>
        </Nav>;


    return (
        <Navbar inverse collapseOnSelect>
            <Navbar.Header>
                <Navbar.Brand>
                    <Link to="/">News</Link>
                </Navbar.Brand>
                <Navbar.Toggle/>
            </Navbar.Header>
            <Navbar.Collapse>
                {authOrNonAuthNav}
            </Navbar.Collapse>
        </Navbar>

    );
};


const mapStateToProps = (state) => {
    return {
        user: state.user,
        displaySearchBar: !(state.visibilityFilter === filters.SHOW_BY_ID),
    }
};
const mapDispatchToProps = (dispatch, ownProps) => {
    return {
        handleNavBarSelect: (eventKey) => {
            switch (eventKey) {
                case event.LOGOUT:
                    localStorage.clear();
                    dispatch(setUser(null));
                    ownProps.history.push('/');
                    return;
                case event.LOGIN:
                    ownProps.history.push('/login');
            }
        },
        handleSearchBar: (searchText) => {
            dispatch(setSearchText(searchText));
            console.log(searchText);
            const visibilityFilter = searchText ?
                filters.SHOW_BY_SEARCH : filters.SHOW_ALL;
            console.log(visibilityFilter);
            dispatch(setVisibilityFilter(visibilityFilter));

        },

    }
};

Header = connect(
    mapStateToProps,
    mapDispatchToProps
)(Header);


export default withRouter(Header);
