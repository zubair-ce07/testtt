import Url from "domurl";

var searchUrl = new Url(
  "https://www.googleapis.com/youtube/v3/search?key=AIzaSyB4UGLPtYbCABbRM6B8MtJgRF1nQaNhUHs"
);
// videoUrl = new Url(
//   "https://www.googleapis.com/youtube/v3/videos?key=AIzaSyB4UGLPtYbCABbRM6B8MtJgRF1nQaNhUHs"
// );

function search(callback, query) {
  searchUrl.query.q = query;
  searchUrl.query.part = "snippet";

  let request = new Request(searchUrl.toString());
  fetch(request)
    .then(response => {
      return response.json();
    })
    .then(callback);
}

// function video(callback, id) {
//   videoUrl.query.id = "";
//   videoUrl.query.part = "snippet";

//   let request = new Request(videoUrl.toString());

// }

export { search };
