export default (state = { clicks: 0 }, action) => {
  switch (action.type) {
    case 'SIMPLE_ACTION':
      return {
        clicks: state.clicks + 1
      };
    default:
      return state;
  }
};
