import React from 'react';

const Loader = (props) => (
     props.isFetching ? <div > Loading...</div> : null
)
export default Loader