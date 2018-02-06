export default class Registration{
    registerFreelancer(username, password, onRegistration) {
        this.register(username, password, "Freelancer", onRegistration);
    }
    registerRecruiter(username, password, onRegistration) {
        this.register(username, password, "Recruiter", onRegistration);
    }
    register(username, password, group, onRegistration) {
        console.log("Regsitration For", "Freelancer");
        var payload = { username: username,
                        password: password,
                        group: "Freelancer" }
        var headers = new Headers();
        headers.append("Content-Type", "application/json;charset=UTF-8");
        var config = {
            method: 'post',
            headers: headers,
            body:JSON.stringify(payload)
        }
        var request = new Request('http://127.0.0.1:8000/register_user', config);
        fetch(request)
          .then((promise) => promise.json())
          .then((response) => {
            if(response.result==="success")
            {
                console.log("Regsitration", "Success");
                onRegistration(true, null);
            }
            else
            {
                 console.log("Regsitration", "Failed");
                 onRegistration(false, response.errors);
            }
          })
          .catch((error) => {
            console.log(error);
          }); 
    }

    
}
