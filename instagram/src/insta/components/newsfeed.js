import React from 'react';

import NavigationBar from './navigationBar'

class Newsfeed extends React.Component{
    render(){
        return(
            <div>
                <NavigationBar/>
                <div className="container-fluid col-sm-12 main-container">
                    {/*<NavigationBar/>*/}
                    <h4>Newsfeed..</h4>
                </div>
            </div>
        )
    }
}

export default Newsfeed