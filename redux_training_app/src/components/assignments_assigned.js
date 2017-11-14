import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router';

import assignmentsAssigned from '../actions/assignments_assigned';


class AssignmentsAssigned extends React.Component
{
    componentWillMount()
    {
        this.props.assignmentsAssigned(this.props.id);
    }

    render()
    {
        const assignments = this.props.assignments;

        if(assignments)
        {
            return (
                <div>
                    {
                        assignments.length === 0
                            ? <p>No Assignments Assigned Yet</p>
                            : assignments.map(assignment => {
                                const title = assignment.title;
                                return (
                                    <Link key={assignment.id}
                                          to={`/assignments/${assignment.id}`}
                                          className="list-group-item">
                                        <h4 className="list-group-item-heading">
                                            { title }
                                        </h4>
                                    </Link>
                                )
                            })
                    }
                </div>
            )
        }
        else
            return <div>Loading...</div>
    }
}

function mapStateToProps(state)
{
    return { assignments: state.assignmentsAssigned.assignmentsAssigned }
}

export default connect(mapStateToProps, { assignmentsAssigned })(AssignmentsAssigned)