import React from 'react';

import { connect } from "react-redux";
import { browserHistory } from 'react-router';

import { retrieveProfile } from '../actions/retrieve_profile';
import { TRAINING_DOMAIN } from '../config';
import NavBar from "./navbar";
import TraineesAssigned from "./trainees_assigned";
import TrainerAssigned from "./trainer_assigned";
import AssignmentsAssigned from "./assignments_assigned";
import ImageUpdation from "./update_image";

class Profile extends React.Component
{
    componentWillMount()
    {
        this.props.retrieveProfile();
        if(!localStorage.getItem('token'))
        {
            browserHistory.push('/');
        }
    }

    render()
    {
        if(this.props.user_profile)
        {
            const user = this.props.user_profile.data;
            const imgPath = TRAINING_DOMAIN + user.user_profile.picture;
            const name = user.user_profile.name;
            const status = user.trainer ? 'Trainer' : 'Trainee';

            return (
                <div>
                    <NavBar/>
                    <div className="container">
                        <div id="s" className="row">
                            <div className="col-sm-4">
                                <img src={ imgPath } className="img-thumbnail"
                                     width="300" height="300"/>
                                <ImageUpdation/>
                            </div>
                            <div className="col-sm-8">
                                <div className="jumbotron">
                                    <h2><strong>{ name }</strong></h2>
                                    <h2><strong>Status</strong>: { status }</h2>
                                    {
                                        (status === 'Trainer')
                                        ? <div>
                                            <h2><strong>Trainees Assigned:</strong></h2>
                                            <TraineesAssigned id={ user.trainer }/>
                                          </div>
                                        : <div>
                                            <h2><strong>Trainer Assigned:</strong></h2>
                                            <TrainerAssigned id={ user.trainee }/>
                                            <br/>
                                            <h2><strong>Assignments Assigned:</strong></h2>
                                            <AssignmentsAssigned id={ user.trainee }/>
                                          </div>
                                    }
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            );
        }
        else
            return (
                <div>
                    Loading...
                </div>
            );
    }
}

function mapStateToProps(state)
{
    return {'user_profile': state.profile.loggedInUser };
}

export default connect(mapStateToProps, { retrieveProfile })(Profile);