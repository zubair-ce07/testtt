import React, {Component} from 'react';
import {connect} from "react-redux";
import {Link} from 'react-router-dom';

import {searchMovie, requestingSearchMovie} from '../../actions/search_actions';
import {HOME, CALENDAR, EXPLORE, SEARCH, TOWATCH, UPCOMING, WATCHED} from '../../utils/page_types';

class SideNav extends Component {
    render() {
        const {active_page} = this.props;
        if(!this.props.isAuthenticated)
            return <div/>;

        return (
            <div className="sidebar">
                <ul>
                    <li className={`sidebar-search ${active_page === SEARCH? 'active': null}`}>
                        <div className="input-group">
                            <input type="text" className="form-control search-input"
                                   placeholder="Search..." onFocus={() => this.props.onFocusOnSearchBar()} onKeyUp={
                                event => {
                                    let query = event.target.value;
                                    query = query.trim();
                                    if (query !== '' && (event.which === 32 || event.which === 13)) {
                                        this.props.requestingSearchMovie();
                                        this.props.searchMovie(event.target.value);
                                    }
                                }
                            }/>
                        </div>
                    </li>
                    <li className={active_page === HOME? 'active': null}><i className="fa fa-dashboard"/>
                        <Link to="/"> Home</Link></li>
                    <li className={active_page === WATCHED? 'active': null}><i className="fa fa-eye"/>
                        <Link to="/watchlist/watched/"> Watched</Link></li>
                    <li className={active_page === TOWATCH? 'active': null}><i className="fa fa-archive"/>
                        <Link to="/watchlist/to-watch/"> To Watch</Link></li>
                    <li className={active_page === UPCOMING? 'active': null}><i className="fa fa-bus"/>
                        <Link to="/watchlist/upcoming/"> Upcoming</Link></li>
                    <li className={active_page === CALENDAR? 'active': null}><i className="fa fa-calendar"/>
                        <Link to="/calendar/"> Calendar</Link></li>
                    <li className={active_page === EXPLORE? 'active': null}><i className="fa fa-camera"/>
                        <Link to="/genres/28/movies/"> Explore</Link></li>
                </ul>
            </div>
        );
    }
}
function mapStateToProps({auth_user, active_page}) {
    return {isAuthenticated: auth_user.isAuthenticated, active_page};
}

export default connect(mapStateToProps, {searchMovie, requestingSearchMovie})(SideNav);
