export const loginUser = ({ username, password }, setSigningIn) => dispatch => {
  console.log(username, password);
  // signing in the user started
  setSigningIn(true);
  // api request
  setTimeout(() => setSigningIn(false), 2000);
};
