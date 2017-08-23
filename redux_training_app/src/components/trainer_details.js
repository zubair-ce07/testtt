import React from 'react';
import { connect } from 'react-redux';

import { retrieveTrainerDetails } from "../actions/retrieve_trainer"
import TraineesAssigned from './trainees_assigned';
import NavBar from "./navbar";

class TrainerDetails extends React.Component
{
    componentWillMount()
    {
        this.props.retrieveTrainerDetails(this.props.params.id);
    }

    render()
    {
        if (this.props.trainer)
        {
            const trainer = this.props.trainer.user;
            const imgPath = trainer.user_profile.picture;
            const name = trainer.user_profile.name;
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
                                    <h2><strong>Status</strong>: Trainer </h2>
                                    <h2><strong>Trainees Assigned:</strong></h2>
                                    <br/>
                                    <TraineesAssigned id={ this.props.params.id }/>
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
    return { trainer: state.selectedUser.selectedUser }
}

export default connect(mapStateToProps, { retrieveTrainerDetails })(TrainerDetails);