export default class API {

    url = (method) => {
        return 'http://127.0.0.1:8000/'+method;
    }

    authorize = (credentials) => {
        var payload = { username: credentials.name,
                        password: credentials.password };
        return fetch(this.url("auth"), {
            method: 'POST',
            mode: 'cors',
            headers: {
                "Content-Type": "application/json;charset=UTF-8"
            },
            body:JSON.stringify(payload)
        }).then(response => response.json());
    }

    freelancers = (token) => {
        return fetch(this.url("freelancers"), {
            method: 'GET',
            mode: 'cors',
            headers: {
                "Authorization" : "Token "+token
            } }).then(response => response.json());
    } 
    
    user = (token) => {
        return fetch(this.url("users"), {
            method: 'GET',
            mode: 'cors',
            headers: {
                "Authorization" : "Token "+token
            }
            }).then(response => response.json());
    }
}


