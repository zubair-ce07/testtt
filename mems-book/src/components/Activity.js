import React from 'react';


export default function Activity(props) {
    return (
        <li className="list-group-item">You <b color="blue">{props.activity.activity }</b> Memory with title
        <b color="blue">"{props.activity.memory_title }" </b> at {props.activity.datetime }</li>
    );
}