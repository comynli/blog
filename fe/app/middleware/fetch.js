/**
 * Created by comyn on 16-11-5.
 */
import encode from 'querystring/encode'

const TOKEN_HEADER = 'X-Authorization-Token';
const TOKEN_KEY = 'token';

export const PAYLOAD = Symbol('PAYLOAD');
export const FETCH_ERROR = 'FETCH_ERROR';
export const UNAUTHORIZED = 'UNAUTHORIZED';
export const FORBIDDEN = 'FORBIDDEN';

export const STATUS_REQUEST = Symbol('STATUS_REQUEST');
export const STATUS_SUCCESS = Symbol('STATUS_SUCCESS');

export function createTypes(name) {
    const types = new Map();
    types.set('request', `request@${name}`);
    types.set('success', `success@${name}`);
    types.set('failure', `failure@${name}`);
    return types;
}

export function setToken(token) {
    localStorage.setItem(TOKEN_KEY, token);
}

export function cleanToken(token) {
    localStorage.removeItem(TOKEN_KEY);
}

export default store => next => action => {
    const payload = action[PAYLOAD];
    if (payload === undefined) {
        next(action);
        return;
    }
    let {endpoint, params, options, post} = payload;
    if (typeof endpoint === 'function') {
        endpoint = endpoint(store.getState())
    }
    if (typeof endpoint !== 'string') {
        new Error('endpoint must be string')
    }
    
    options = options || {};
    if (typeof post !== 'function') {
        post = data => data;
    }
    
    const types = payload.types;
    if (! types instanceof Map) {
        new Error('types must be Map');
    }
    if (types.has('request') || typeof types.get('request') !== 'string') {
        new Error('type of request must be string')
    }
    if (types.has('success') || typeof types.get('success') !== 'string') {
        new Error('type of success must be string')
    }
    if (types.has('failure') || typeof types.get('failure') !== 'string') {
        new Error('type of success must be string')
    }

    let url = `${endpoint}`;
    if (params) {
        url = `${url}?${encode(params)}`
    }
    let headers = options.headers;
    if (!headers) {
        headers = new Headers({'Content-Type': 'application/json'})
    }

    const token = localStorage.getItem('token');
    if (token) {
        headers.set(TOKEN_HEADER, token)
    }
    options.headers = headers;
    
    const actionWith = data => {
        const finalAction = Object.assign({}, action, data);
        delete finalAction[PAYLOAD];
        return finalAction;
    };
    next(actionWith({type: types.get('request')}));
    
    return fetch(url, options).then(res => {
        if (res.ok) {
            res.json().then(data => next(actionWith({res: post(data), type: types.get('success')})))
        } else {
            switch (res.status) {
                case 401:
                    next(actionWith({type: UNAUTHORIZED, fetch_type: types.get('failure')}));
                    break;
                case 403:
                    next(actionWith({type: FORBIDDEN, fetch_type: types.get('failure')}));
                    break;
                default:
                    next(actionWith({type: FETCH_ERROR, fetch_type: types.get('failure'), status: res.status}));
            }
        }
    }).catch(err => console.log(err));
}