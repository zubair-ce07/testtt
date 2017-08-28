import * as React from "react";
import {connect} from "react-redux";
import {actions, filters} from "../config";


const Link = (props) => {
    return (
        <button
            onClick={props.onClick}
            disabled={props.active}
        >
            {props.children}
        </button>
    );
};


const mapStateToLinkProps = (state, ownProps) => {
    return ({
        active: ownProps.filter === state.visibilityFilter
    });
};
const mapDispatchToLinkProps = (dispatch, ownProps) => {
    return ({
        onClick: (() => dispatch({
            type: actions.SET_VISIBILITY_FILTER,
            filter: ownProps.filter,
        }))
    })
};
const FilterLink = connect(
    mapStateToLinkProps,
    mapDispatchToLinkProps
)(Link);


const FilterLinks = () => {
    return (
        <div className="filerLinks">
            <FilterLink filter={filters.SHOW_ALL}>
                All
            </FilterLink>
            <FilterLink filter={filters.SHOW_COMPLETED}>
                Completed
            </FilterLink>
            <FilterLink filter={filters.SHOW_UNCOMPLETED}>
                Uncompleted
            </FilterLink>
        </div>
    );
};

export default FilterLinks;
