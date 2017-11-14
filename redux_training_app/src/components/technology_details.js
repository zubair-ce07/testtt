import React from 'react';
import { connect } from 'react-redux';

import { retrieveTechnologyDetails } from '../actions/retrieve_technology';
import NavBar from './navbar';


class AssignmentDetails extends React.Component
{
    componentWillMount()
    {
        this.props.retrieveTechnologyDetails(this.props.params.id);
    }

    render()
    {
        let technology = this.props.technology;
        if(technology)
        {
            return (
                <div>
                    <NavBar/>
                    <div className="container">
                        <div className="jumbotron">
                            <h2>
                                <strong>Title :</strong> { technology.name}
                            </h2>
                            <br/>
                            <h3>
                                <strong>Description :</strong>
                                <p>{ technology.description }</p>
                            </h3>
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
    return { technology: state.technologyDetails.selectedTechnology }
}

export default connect(mapStateToProps, { retrieveTechnologyDetails })(AssignmentDetails);