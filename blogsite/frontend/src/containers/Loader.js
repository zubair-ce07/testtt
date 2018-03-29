import React from 'react';


const Loader = (props) => (

    <div>
        {
            props.isFetching &&
            <div > Loading...</div>
        }

    </div>
);

export default Loader


