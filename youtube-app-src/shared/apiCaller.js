export const fetchData = (url, callback) => {
  return fetch(url)
    .then(response => response.json())
    .then(result => callback(result))
    .catch(console.error);
};
