
export default class Auth{
    
    constructor(){
        this.authenticate = this.authenticate.bind(this);
        this.isAuthenticated = this.isAuthenticated.bind(this);
        this.getHeaders = this.getHeaders.bind(this);
        this.reset = this.reset.bind(this);
    }

    authenticate(username, password, onAuthentication) {
        console.log("Authentication", "Begin");
        var payload = { username: username,
                        password: password }
        var headers = new Headers();
        headers.append("Content-Type", "application/json;charset=UTF-8");
        var config = {
            method: 'post',
            headers: headers,
            body:JSON.stringify(payload)
        }
        var request = new Request('http://127.0.0.1:8000/auth', config);
        fetch(request)
          .then((promise) => promise.json())
          .then((response) => {
            console.log("Authentication", "Success");
            this.setSession(response);
            onAuthentication(true)
          })
          .catch((error) => {
            console.log(error);
          }); 
    }
    reset(){
        localStorage.removeItem('access_token');
    }
    setSession(authResult) {
        localStorage.setItem('access_token', authResult.token);
    }
    getHeaders(){
        var headers = new Headers();
        let session_key = localStorage.getItem('access_token');
        headers.append("Authorization","Token "+session_key);
        return headers;
    }
    isAuthenticated() {
    // Check whether the current time is past the
    // access token's expiry time
    let session_key = localStorage.getItem('access_token');
    console.log(session_key);
    if(session_key !== "undefined" && session_key){
    // let token = JSON.parse(localStorage.getItem('access_token'));
    console.log(session_key);
        // if(token){
    console.log("Logged In","true");
    return true;
        // }
    }
    console.log("Logged In", "false");
    return false;

  }


}
