import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router';

import { trainerAssigned } from "../actions/trainer_assigned"

class TrainerAssigned extends React.Component
{
    componentWillMount()
    {
        this.props.trainerAssigned(this.props.id);
    }

    render()
    {
        const trainer = this.props.trainer;
        if (trainer)
        {
            const name = trainer.user.user_profile.name;
            return (
                <Link key={trainer.id}
                      to={`/trainers/${trainer.id}`}
                      className="list-group-item">
                    <h4 className="list-group-item-heading">
                        { name }
                    </h4>
                </Link>
            )
        }
        else
            return <div>Loading...</div>
    }
}

function mapStateToProps(state)
{
    return { trainer: state.trainerAssigned.trainerAssigned }
}

export default connect(mapStateToProps, { trainerAssigned })(TrainerAssigned);