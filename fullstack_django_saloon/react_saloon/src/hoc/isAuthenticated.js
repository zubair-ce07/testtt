import React from 'react';
import ls from 'local-storage';
import PropTypes from 'prop-types';
import { routeConstants } from '../constants/routeConstants';
import { reactAppConstants } from '../constants/constants';

const IsAuthenticated = WrappedComponent => {
    const checkIsAuthenticated = (props) => {
        if (!ls.get('token')) {
            props.history.push(routeConstants.LIST_SALOONS_ROUTE);
        }
        else if (props.match.path === routeConstants.MY_SALOON_ROUTE && ls.get(reactAppConstants.USER_TYPE) !== reactAppConstants.SALOON) {
            props.history.push(routeConstants.LIST_SALOONS_ROUTE);
        }
        else if (props.match.path === routeConstants.SLOT_LIST_ROUTE && ls.get(reactAppConstants.USER_TYPE) !== reactAppConstants.CUSTOMER) {
            props.history.push(routeConstants.LIST_SALOONS_ROUTE);
        }
        return (
            <React.Fragment>
                <WrappedComponent {...props} />
            </React.Fragment>
        );
    };
    checkIsAuthenticated.propTypes = {
        history: PropTypes.object.isRequired,
        match: PropTypes.object.isRequired,
    };
    return checkIsAuthenticated;
};
export default IsAuthenticated;