import React from 'react';
import Moment from 'moment';

import {Link} from "react-router-dom";


const FollowRequest = ({follow_request, onAccept, onBlock}) => {
    const from_user = follow_request.actor;

    return (
        <div className="request-item row">
            <div className="col-md-3 p-0">
                <img src={from_user.photo === null? '/images/avatar.jpg': from_user.photo} height={60} width={60}/>
            </div>
            <div className="col-md-9 pr-0">
                <h6 className="mb-1"><Link
                    to={`/users/${from_user.id}/`}>{`${from_user.first_name} ${from_user.last_name}`}</Link></h6>
                {follow_request.action_object.status === 'New' &&
                <div className="row ml-0 mr-0">
                    <div className="col-md-6 p-0">
                        <button className="btn btn-success font-11 py-0"
                                onClick={() => onAccept(follow_request.action_object.id)}>Accept
                        </button>
                    </div>
                    < div className="col-md-6 p-0">
                        <button className="btn btn-secondary font-11 py-0"
                                onClick={() => onBlock(follow_request.action_object.id)}>Block
                        </button>
                    </div>
                </div>
                }
                {follow_request.action_object.status !== 'New' &&
                    <div className="row mx-0 text-center">
                        <button className="btn btn-info disabled font-11 py-0 mt-1 mx-auto">{follow_request.action_object.status}</button></div>}
                <h6 className="font-11 float-right mt-1 mb-0">{Moment(follow_request.timestamp).calendar()}</h6>
            </div>
        </div>
    );
};

export default FollowRequest;
