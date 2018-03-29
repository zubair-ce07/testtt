import axios from 'axios';
axios.defaults.headers.common['Authorization'] = 'apple';
class categoryApi {

    static getCategoryData() {
        var url='http://localhost:3001/categories';
        return axios.get(url)
            .then(response => {
                return response.data;
            }).catch(error => {
                return error;
            });
    }
    static getPostsOfCategory(category) {
        var url=`http://localhost:3001/${category}/posts`;
        return axios.get(url)
            .then(response => {
                return response.data;
            }).catch(error => {
                return error;
            })
    }

}

export default categoryApi;
