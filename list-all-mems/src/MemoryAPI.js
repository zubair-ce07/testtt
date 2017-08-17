import * as constants from './Constants';
class MemoryAPI {
    getAllMems(){
        return fetch(constants.GETALLMEMSURL).then((response) => response.json())
        .then((responseData) => {
          return responseData;
        })
        .catch(error => console.warn(error));
      }

    addMemory(memory){
        return fetch(constants.GETALLMEMSURL,
            {
                method: "POST",
                headers: {
                  'Accept': 'application/json, text/plain, */*',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(memory)
            }
        ).then((response) => response.json())
        .then((responseData) => {
            alert(responseData);
          return responseData;
        })
        .catch(error => {
            console.warn(error);
        });

    }
}
export default MemoryAPI;
