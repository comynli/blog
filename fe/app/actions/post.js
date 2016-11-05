/**
 * Created by comyn on 16-11-5.
 */
import {PAYLOAD, createTypes} from '../middleware/fetch';


export const CREATE_POST_TYPES = createTypes('create_post');
export function create(catalog) {
    return dispatch => dispatch({
        [PAYLOAD]: {
            types: CREATE_POST_TYPES,
            endpoint: '/api/post',
            params: {catalog},
            options: {method: 'PUT'}
        }
    })
}