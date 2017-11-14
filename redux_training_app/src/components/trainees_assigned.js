import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router';

import { traineesAssigned } from '../actions/trainees_assigned';

class TraineesAssigned extends React.Component
{
    componentWillMount()
    {
        this.props.traineesAssigned(this.props.id);
    }

    render()
    {
        const trainees = this.props.trainees;
        if(trainees)
        {
            return (
                <div className="container list-group">
                    {
                        trainees.map(trainee => {
                            const name = trainee.user.user_profile.name;
                            return (
                                <Link key={trainee.id}
                                      to={`/trainees/${trainee.id}`}
                                      className="list-group-item">
                                    <h4 className="list-group-item-heading">
                                        { name }
                                    </h4>
                                </Link>
                            )
                        })
                    }
                </div>
            )
        }
        else
        {
            return <div>Loading...</div>
        }
    }
}

function mapStateToProps(state)
{
    return { trainees: state.traineesAssigned.traineesAssigned }
}

export default connect(mapStateToProps, { traineesAssigned })(TraineesAssigned);