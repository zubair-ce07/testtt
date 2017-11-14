import React from 'react';
import { connect } from 'react-redux';

import { retrieveAssignmentDetails } from '../actions/retrieve_assignment';
import NavBar from './navbar';
import TechnologyUsed from './technologies_used';


class AssignmentDetails extends React.Component
{
    componentWillMount()
    {
        this.props.retrieveAssignmentDetails(this.props.params.id);
    }

    render()
    {
        let assignment = this.props.assignment;
        if(assignment)
        {
            return (
                <div>
                <NavBar/>
                    <div className="container">
                        <div className="jumbotron">
                            <h2>
                                <strong>Title :</strong> { assignment.title }
                            </h2>
                            <br/>
                            <h3>
                                <strong>Description :</strong>
                                <p>{ assignment.description }</p>
                            </h3>
                            <br/>
                            {
                                assignment.completion_status
                                    ? <h3><strong> Assignment Completed </strong></h3>
                                    : <h3><strong> Assignment Not Completed Yet </strong></h3>
                            }
                            <br/>
                            <h3><strong>Technologies Used :</strong></h3>
                            <TechnologyUsed id={this.props.params.id}/>
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
    return { assignment: state.assignmentDetails.selectedAssignment }
}

export default connect(mapStateToProps, { retrieveAssignmentDetails })(AssignmentDetails);