import React from 'react';
import { connect } from 'react-redux';

import { retrieveTraineeDetails } from "../actions/retrieve_trainee";
import TrainerAssigned from './trainer_assigned';
import NavBar from "./navbar";
import AssignmentsAssigned from './assignments_assigned';

class TraineeDetails extends React.Component
{
    componentWillMount()
    {
        this.props.retrieveTraineeDetails(this.props.params.id);
    }

    render()
    {
        if (this.props.trainee)
        {
            const trainee = this.props.trainee.user;
            const imgPath = trainee.user_profile.picture;
            const name = trainee.user_profile.name;
            return (
                <div>
                    <NavBar/>
                    <div className="container">
                        <div className="row">
                            <div className="col-sm-4">
                                <img src={ imgPath } className="img-thumbnail"
                                     width="300" height="300"/>
                            </div>
                            <div className="col-sm-8">
                                <div className="jumbotron">
                                    <h2><strong>{ name }</strong></h2>
                                    <h2><strong>Status</strong>: Trainee </h2>
                                    <h2><strong>Trainer Assigned:</strong></h2>
                                    <TrainerAssigned id={ this.props.params.id }/>
                                    <br/>
                                    <h2><strong>Assignments Assigned:</strong></h2>
                                    <AssignmentsAssigned id={ this.props.params.id }/>
                                </div>
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
    return { trainee: state.selectedUser.selectedUser }
}

export default connect(mapStateToProps, { retrieveTraineeDetails })(TraineeDetails);