/**
 * Created by comyn on 16-10-29.
 */
import React from 'react';
import ReactDOM from 'react-dom';
import Provider from 'react-redux/lib/components/Provider';
import store from './store';
import routes from './routes';

const root = document.getElementById("root");

ReactDOM.render(
    <Provider store={store}>
        {routes}
    </Provider>, root);

if (module.hot) {
    module.hot.accept('./reducers', () => {
        const nextReducer = require('./reducers');
        store.replaceReducer(nextReducer);
    })
}
