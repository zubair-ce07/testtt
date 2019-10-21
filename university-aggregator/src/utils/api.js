import axios from 'axios';

export const api = axios.create({
  baseURL: `http://127.0.0.1:8000/api/v1/`,
});


api.interceptors.request.use(function (config) {
  config.headers = {
  'Content-Type': 'application/json',
  'Authorization': `Token ${JSON.parse(localStorage.getItem('token')) || ''}`,
  }
  return config;
});