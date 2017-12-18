import React, {Component} from 'react';
import {connect} from "react-redux";
import {Link} from 'react-router-dom';

import {searchMovie, requestingSearch, searchUser} from '../../actions/search_actions';
import {
    HOME,
    CALENDAR,
    EXPLORE,
    SEARCH,
    TOWATCH,
    UPCOMING,
    WATCHED,
    FOLLOWED_BY,
    FOLLOWS
} from '../../utils/page_types';


class SideNav extends Component {
    constructor(props) {
        super(props);

        this.state = {
            search_type: 'movies'
        }
    }

    handleChange(event) {
        this.setState({search_type: event.target.value});
    }

    search(event) {
        let query = event.target.value;
        query = query.trim();
        if (query !== '' && (event.which === 32 || event.which === 13)) {
            this.props.requestingSearch();
            this.state.search_type === 'movies' ? this.props.searchMovie(event.target.value)
                : this.props.searchUser(event.target.value);
        }
    }

    render() {
        const {active_page} = this.props;
        if (!this.props.isAuthenticated)
            return <div/>;

        return (
            <div className="sidebar">
                <ul>
                    <li className={`sidebar-search ${active_page === SEARCH ? 'active' : null}`}>
                        <div className="input-group">
                            <input type="text" className="form-control search-input"
                                   placeholder="Search..." onFocus={() => this.props.onFocusOnSearchBar()}
                                   onKeyUp={event => this.search(event)}/>
                            <span className="input-group-btn">
                                <select className="btn btn-default search-type-select"
                                        onChange={this.handleChange.bind(this)}>
                                    <option value="movies">&#xf008;</option>
                                    <option value="users">&#xf007;</option>
                                </select>
                        </span>
                        </div>
                    </li>
                    <li className={active_page === HOME ? 'active' : null}><i className="fa fa-dashboard"/>
                        <Link to="/"> Home</Link></li>
                    <li className={active_page === WATCHED ? 'active' : null}><i className="fa fa-eye"/>
                        <Link to="/watchlist/watched/"> Watched</Link></li>
                    <li className={active_page === TOWATCH ? 'active' : null}><i className="fa fa-archive"/>
                        <Link to="/watchlist/to-watch/"> To Watch</Link></li>
                    <li className={active_page === UPCOMING ? 'active' : null}><i className="fa fa-bus"/>
                        <Link to="/watchlist/upcoming/"> Upcoming</Link></li>
                    <li className={active_page === CALENDAR ? 'active' : null}><i className="fa fa-calendar"/>
                        <Link to="/calendar/"> Calendar</Link></li>
                    <li className={active_page === EXPLORE ? 'active' : null}><i className="fa fa-camera"/>
                        <Link to="/genres/28/movies/"> Explore</Link></li>
                    <li className={active_page === FOLLOWS ? 'active' : null}><i className="fa fa-user"/>
                        <Link to="/network/follows/"> Follows</Link></li>
                    <li className={active_page === FOLLOWED_BY ? 'active' : null}><i className="fa fa-user-o"/>
                        <Link to="/network/followings/"> Followings</Link></li>
                </ul>
            </div>
        );
    }
}
function mapStateToProps({auth_user, active_page}) {
    return {isAuthenticated: auth_user.isAuthenticated, active_page};
}

export default connect(mapStateToProps, {searchMovie, requestingSearch, searchUser})(SideNav);
