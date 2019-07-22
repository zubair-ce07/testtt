## Directions

1. Clone/download the repository
2. Open the `search.html` file in a browser
3. Make a search and follow pretty self-explanatory UI

## Known Limitations

1. Country form submits itself and reloads the page when `Return` is pressed. This event has not yet been handled.

2. Multiple requests are made to the server if a user keeps clicking the tabs in `user.html`. A check has to be in place to identify if a request was already made and the data is available in the DOM
