import { createStore, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import rootReducer from './reducers';

export default function configureStore(initialState = {}) {
  const store = createStore(
    rootReducer,
    applyMiddleware(thunk)
  );

  // eslint-disable-next-line
  if (module.hot) {
    // eslint-disable-next-line
    module.hot.accept('./reducers', () => {
      store.replaceReducer(rootReducer);
    });
  }

  return store;
}
