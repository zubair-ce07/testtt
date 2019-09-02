import axios from "axios";

const backend = axios.create({
  baseURL: "http://localhost:8000"
});

backend.interceptors.response.use(
  response => response,
  error => Promise.reject(error.response)
);

export default backend;
