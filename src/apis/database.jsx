import axios from "axios";

const backend = axios.create({
  baseURL: "http://localhost:8000"
});

backend.interceptors.response.use(
  response => response,
  error => {
    const errorResponse = error.response;

    console.log("ima intevetpp", errorResponse);

    // if (isTokenExpired(errorResponse)) {
    //   return resetTokenAndReattempRequest();
    // }

    return Promise.reject(error.response);
  }
);

// const isTokenExpired = response => {
//   // console.log("response", response);
// };

// const resetTokenAndReattempRequest = () => {
//   // console.log("reateempting request");
// };

export default backend;
