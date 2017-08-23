import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router';

import NavBar from './navbar';
import { changeSearchPage } from "../actions/change_search_page";
import {searchUsers} from "../actions/search_users";


class SearchResults extends React.Component
{
    componentWillMount()
    {
        if(!this.props.searchResults)
        {
            this.props.searchUsers(this.props.params.q);
        }
    }

    nextPage()
    {
        this.props.changeSearchPage(this.props.searchResults.next);
    }

    prevPage()
    {
        this.props.changeSearchPage(this.props.searchResults.previous);
    }

    renderUserList(result)
    {
        let user_profile = result.user_profile;
        let status = result.trainer ? 'Trainer' : 'Trainee';
        return (
            <Link key={user_profile.user}
                  to={status==='Trainer' ? `/trainers/${result.trainer}`
                      : `/trainees/${result.trainee}`}
                  className="list-group-item">
                <h4 className="list-group-item-heading">
                    { user_profile.name }
                </h4>
                <p className="list-group-item-text">
                    { status }
                </p>
            </Link>
        )
    }

    render()
    {
        let searchResults = this.props.searchResults;
        if(searchResults)
        {
            let nextButton = <button className="btn btn-primary disabled" ><div>Next{' '}
                <span id="next" className="glyphicon glyphicon-arrow-right"/></div></button>;
            let prevButton = <button className="btn btn-primary disabled" ><div>
                <span id="prev" className="glyphicon glyphicon-arrow-left"/>{' '}Prev</div></button>;

            if(searchResults.previous)
            {
                prevButton = <button className="btn btn-primary" onClick={ this.prevPage.bind(this) }><div>
                        <span id="prev" className="glyphicon glyphicon-arrow-left"/>{' '}Prev</div></button>;
            }
            if(searchResults.next)
            {
                nextButton = <button className="btn btn-primary" onClick={ this.nextPage.bind(this) }><div>
                    Next{' '}<span id="next" className="glyphicon glyphicon-arrow-right"/></div></button>;
            }
            return (
                <div>
                    <NavBar/>
                    <div className="container list-group">
                        <h2>You searched for: <strong> {this.props.params.q} </strong></h2>
                        {
                            (searchResults.count > 0) ?
                                searchResults.results.map(this.renderUserList)
                            :   <div id="error-msg" className="alert alert-danger">
                                    Results<strong>{' '}not{' '}</strong>Found
                                </div>
                        }
                        <div className="btn-group btn-group-justified">
                            <div className="btn-group">
                            { prevButton }
                            </div>
                            <div className="btn-group">
                                { nextButton }
                            </div>
                        </div>
                    </div>
                </div>
            )
        }
        else
            return <div>Loading...</div>
    }
}

function mapStateToProps(state)
{
    return { searchResults: state.search.searchedUsers }
}

export default connect(mapStateToProps, { changeSearchPage, searchUsers })(SearchResults);