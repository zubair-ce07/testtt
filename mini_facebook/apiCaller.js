function callApi(url)
{
  fetch(url)
    .then(response => response.json())
    .then(data =>
    {
      return data;
    })
    .catch(console.error);
}

export {callApi};