import Auth from '../services/auth.jsx';

export default class User{

	constructor(props) {
		this.get = this.get.bind(this);
	}

	get(){
		let auth = new Auth()
		if(auth.isAuthenticated()){
			return this.requestUserDetails(auth.getHeaders())
		}
	}
	requestUserDetails(headers){
        console.log("User Fetch", "Begin");
        var config = {
            method: 'get',
            headers: headers,
        }
        var request = new Request('http://127.0.0.1:8000/current_user', config);
        
        return fetch(request)
          .then((promise) => {
          	console.log("Request","Resolved");
          	console.log("Response",promise);
          	return promise.json()

          });
          

	}
}
