import React from 'react';
import {UncontrolledTooltip} from "reactstrap";

export const Counters = ({movie}) => {
    return <div className="text-center">
        <i className="fa fa-plus-square counters" id={"add" + movie.id}> {movie.counts.added}</i>
        <i className="fa fa-eye counters" id={"watch" + movie.id}> {movie.counts.watched}</i>
        <i className="fa fa-thumbs-up counters" id={"likes" + movie.id}> {movie.counts.likes}</i>
        <i className="fa fa-thumbs-down counters" id={"dislikes" + movie.id}> {movie.counts.dislikes}</i>
        <i className="fa fa-reply counters" id={"recommend" + movie.id}> {movie.counts.recommended}</i>
        <i className="fa fa-star counters" id={"rating" + movie.id}> {movie.vote_average}</i>
        <UncontrolledTooltip placement="top" target={"add" + movie.id}>Added</UncontrolledTooltip>
        <UncontrolledTooltip placement="top" target={"watch" + movie.id}>Watched</UncontrolledTooltip>
        <UncontrolledTooltip placement="top" target={"likes" + movie.id}>Liked</UncontrolledTooltip>
        <UncontrolledTooltip placement="top" target={"dislikes" + movie.id}>Disliked</UncontrolledTooltip>
        <UncontrolledTooltip placement="top" target={"recommend" + movie.id}>Recommended</UncontrolledTooltip>
        <UncontrolledTooltip placement="top" target={"rating" + movie.id}>Rating</UncontrolledTooltip>
    </div>;
};