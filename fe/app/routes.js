/**
 * Created by comyn on 16-11-5.
 */
import React from 'react';
import {Router, Route, browserHistory} from 'react-router';
import App from './App';
import Login from './containers/Login';
import Editor from './containers/Editor';

const routes = (
    <Router history={browserHistory}>
        <Route path="/" component={App}>
            <Route path="login" component={Login} />
            <Route path="edit" component={Editor} />
            
        </Route>
    </Router>
);

export default routes;