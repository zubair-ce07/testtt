var fun = function getAllMems() {
    fetch('http://127.0.0.1:8000/get-all-mems/').then(response => {
             response.json().then(data => {
                 return data[0];
             });
        });
}
export default fun;