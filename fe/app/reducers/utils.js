/**
 * Created by comyn on 16-11-5.
 */
import uuid from 'node-uuid';
import {STATUS_REQUEST, STATUS_SUCCESS} from '../middleware/fetch';

const initialState = {
    res: null,
    status: null,
    type: null,
    id: uuid.v4()
};


export function createReducer(...types) {
    const requests = types.map(it => it.get('request'));
    const successes = types.map(it => it.get('success'));
    
    return (state = initialState, action) => {
        switch (true) {
            case requests.indexOf(action.type) >= 0:
                return Object.assign({}, state, {
                    status: STATUS_REQUEST,
                    type: action.type,
                    id: uuid.v4()
                });
            case successes.indexOf(action.type) >= 0:
                return Object.assign({}, state, {
                    res: action.res,
                    status: STATUS_SUCCESS,
                    type: action.type,
                    id: uuid.v4()
                });
            default:
                return state;
        }
    }
}