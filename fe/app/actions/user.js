/**
 * Created by comyn on 16-11-5.
 */
import {PAYLOAD, createTypes} from '../middleware/fetch';

export const LOGIN_TYPES = createTypes('login');
export function login(mail, password) {
    return dispatch => dispatch({
        [PAYLOAD]: {
            types: LOGIN_TYPES,
            endpoint: '/api/user/login',
            options: {method: 'POST', body: JSON.stringify({mail, password})}
        }
    })
}