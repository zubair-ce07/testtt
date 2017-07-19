import Url from "domurl";

var searchUrl = new Url(
  "https://www.googleapis.com/youtube/v3/search?&key=AIzaSyB4UGLPtYbCABbRM6B8MtJgRF1nQaNhUHs"
);

function search(callback, query) {
  searchUrl.query.q = query;
  searchUrl.query.part = "snippet";

  let request = new Request(searchUrl.toString());
  fetch(request).then(response => response.json()).then(callback);
}

export { search };
