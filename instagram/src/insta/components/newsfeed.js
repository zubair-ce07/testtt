import React from 'react';

import {globalVars} from '../utils/common';
import NavigationBar from './navigationBar';


class Newsfeed extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            newsfeed:{},
        };
        this.fetchNewsfeed = this.fetchNewsfeed.bind(this);
    }

    fetchNewsfeed() {
        debugger;
        // fetch(urls.baseURL+urls.newsfeed, {
        //     method: 'post',
        // }).then((response) => {
        //     return response.json()
        // }).then((data) => {
        //     console.log(data)
        // }).catch((error) => {
        //     console.log(error)
        // })
    }

    componentWillMount(){
        // debugger;
        // let headers = new Headers()
        // headers.append('Authorization', 'Basic ' + base64.encode("humdah" + ":" + "admin12345"))
        console.log('fetching newsfeed..');
        console.log(globalVars.isLoggedIn)
        // this.fetchNewsfeed();
        fetch(globalVars.urls.baseURL+globalVars.urls.newsfeed, {
            method: 'get',
            // body: JSON.stringify({
            //         username: this.state.username,
            //         password: this.state.password,
            // }),
            // headers: {
            //     'Content-Type': 'application/json'
            // }
        }).then((response) => {
            return response.json()
        }).then((data) => {
            console.log(data)
        }).catch((error) => {
            console.log(error)
        })
    }

    render(){
        // let urls = globalVars.urls;
        // debugger;
        return(
            <div>
                <NavigationBar/>
                <div className="container-fluid col-sm-12 main-container">
                    {/*<NavigationBar/>*/}
                    <h4>Newsfeed..</h4>
                    {console.log(globalVars)}
                    {/*<h2>{urls.signup}</h2>*/}
                </div>
            </div>
        )
    }
}

export default Newsfeed;