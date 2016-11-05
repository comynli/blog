/**
 * Created by comyn on 16-11-5.
 */
import compose from 'redux/lib/compose';
import createStore from 'redux/lib/createStore';
import applyMiddleware from 'redux/lib/applyMiddleware';
import thunkMiddleware from 'redux-thunk';
import createLogger from 'redux-logger';
import fetchMiddleware from './middleware/fetch';
import rootReducer from './reducers';

const store = compose(
    applyMiddleware(thunkMiddleware),
    applyMiddleware(fetchMiddleware),
    applyMiddleware(createLogger()),
)(createStore)(rootReducer);

export default store;