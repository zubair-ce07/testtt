import React from "react";
import {HealthBar} from "../../components";
import "./HealthStatus.css";

const HealthStatus = props => {
    return (
        <div className="health-status">
            <HealthBar content={props.user.content} percentage={props.user.percentage}/>
            <HealthBar content={props.opponent.content} percentage={props.opponent.percentage}/>
        </div>
    );
}

export {HealthStatus}
