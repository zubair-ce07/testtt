import React from 'react'
import ls from 'local-storage'

const Rainbow = (WrappedComponent) => {

    return (props) => {
        console.log(props)
        if (!ls.get('token')) {
            props.history.push('/')
        }
        else {
            if (props.match.path === '/mysaloon/' && ls.get('user_type') !== 'saloon') {
                props.history.push('/')
            }
            else if (props.match.path === '/:shop_name/' && ls.get('user_type') !== 'customer') {
                props.history.push('/')
            }
        }
        return (
            <React.Fragment>
                <WrappedComponent {...props} />
            </React.Fragment>
        )
    }

}

export default Rainbow