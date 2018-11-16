import { formSourcesList } from './helpers';

export const fetchData = (url, callback) =>
  fetch(url)
    .then(response => response.json())
    .then(result => formSourcesList(result))
    .then(list => callback(list))
    .catch(console.error);
