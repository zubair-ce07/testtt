import Url from "domurl";

var searchUrl = new Url(
  "https://www.googleapis.com/youtube/v3/search?&key=AIzaSyB4UGLPtYbCABbRM6B8MtJgRF1nQaNhUHs"
);

function search(query) {
  searchUrl.query.q = query;
  searchUrl.query.part = "snippet";

  let request = new Request(searchUrl.toString());
  return fetch(request).then(response => response.json()).catch(error => {
    return error;
  });
}

export { search };
