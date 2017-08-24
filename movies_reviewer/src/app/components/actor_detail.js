import React, {Component} from 'react';
import {connect} from 'react-redux';

import {fetchActor} from '../actions/index';
import {getImageUrl} from './movie_detail';

class ActorDetail extends Component {
    componentWillMount() {
        this.props.fetchActor(this.props.match.params.id);
    }

    render() {
        const {actor} = this.props;
        if (!actor)
            return <h3 className="text-center">Loading...</h3>;

        const posterUrl = getImageUrl(actor.profile_path, 'h632');

        return (
            <div>
              <h1 className="page-title">{actor.name}</h1>
              <div className="actor-detail top-element">
                <div className="row">
                  <div className="col-md-4 text-center">
                    <img src={posterUrl} height="400"/>
                  </div>
                  <div className="col-md-8 content">
                    <br/><h5 className="text-center">{actor.tagline}</h5>
                    <br/><h4>Biography: </h4>
                    <p>{actor.biography}</p><br/>
                    <h6><b>Birthday: </b>{actor.birthday}</h6>
                    <h6><b>Place of birth: </b>{actor.place_of_birth}</h6>
                  </div>
                </div>
              </div>
            </div>
        );
    }
}

function mapStateToProps(state, ownProps) {
    const props = {actor: null};
    if(state.actor && state.actor.id === Number(ownProps.match.params.id))
        props["actor"] = state.actor;
    return props;
}

export default connect(mapStateToProps, {fetchActor})(ActorDetail);
