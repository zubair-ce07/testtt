import React from 'react';
import ls from 'local-storage';
import PropTypes from 'prop-types';

const IsAuthenticated = (WrappedComponent) => {

    const checkIsAuthenticated = (props) => {
        if (!ls.get('token')) {
            props.history.push('/');
        }
        else {
            if (props.match.path === '/mysaloon/' && ls.get('user_type') !== 'saloon') {
                props.history.push('/');
            }
            else if (props.match.path === '/:shop_name/' && ls.get('user_type') !== 'customer') {
                props.history.push('/');
            }
        }
        return (
            <React.Fragment>
                <WrappedComponent {...props} />
            </React.Fragment>
        );
    };

    checkIsAuthenticated.propTypes = {
        history: PropTypes.object.isRequired,
        match:PropTypes.object.isRequired,
    
    };

    return checkIsAuthenticated;

};

export default IsAuthenticated;