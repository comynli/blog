/**
 * Created by comyn on 16-11-5.
 */
import {FETCH_ERROR, UNAUTHORIZED, FORBIDDEN} from '../middleware/fetch';

const initialState = {
    type: null,
    fetch_type: null,
    status: null
};

export default function error(state = initialState, action) {
    switch (action.type) {
        case UNAUTHORIZED:
            return {type: UNAUTHORIZED, fetch_type: action.fetch_type, status: 401};
        case FORBIDDEN:
            return {type: FORBIDDEN, fetch_type: action.fetch_type, status: 403};
        case FETCH_ERROR:
            return {type: FETCH_ERROR, fetch_type: action.fetch_type, status: action.status};
        default:
            return state
    }
}