import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router';

import technologiesUsed from '../actions/technologies_used';


class TechnologiesUsed extends React.Component
{
    componentWillMount()
    {
        this.props.technologiesUsed(this.props.id);
    }

    render()
    {
        const technologies = this.props.technologies;
        if(technologies)
        {
            return (
                <div>
                    {
                        technologies.length === 0
                            ? <p>No Technologies Used Yet</p>
                            : technologies.map(technology => {
                                const name = technology.name;
                                return (
                                    <Link key={technology.id}
                                          to={`/technologies/${technology.id}`}
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
            return <div>Loading...</div>
    }
}

function mapStateToProps(state)
{
    return { technologies: state.technologiesUsed.technologiesUsed }
}

export default connect(mapStateToProps, { technologiesUsed })(TechnologiesUsed)