import Auth from '../services/auth.jsx';

export default class Freelancer{

	constructor(props) {
		this.getAll = this.getAll.bind(this);
	}

	getAll(){
		let auth = new Auth()
		if(auth.isAuthenticated()){
			return this.getFreelancers(auth.getHeaders())
		}
		else
		{
			let headers = new Headers();
			return this.getFreelancers(headers)
		}
	}
	getFreelancers(headers){
        console.log("User Fetch", "Begin");
        var config = {
            method: 'get',
            headers: headers,
        }
        var request = new Request('http://127.0.0.1:8000/freelancers', config);
        
        return fetch(request)
          .then((promise) => {
          	console.log("Request","Resolved");
          	console.log("Response",promise);
          	return promise.json()

          });
          

	}
}
