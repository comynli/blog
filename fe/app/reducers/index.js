/**
 * Created by comyn on 16-11-5.
 */
import combineReducers from 'redux/lib/combineReducers';
import error from './error';
import * as utils from './utils';
import * as UserActions from '../actions/user';
import * as PostActions from '../actions/post';

const login = utils.createReducer(UserActions.LOGIN_TYPES);
const post = utils.createReducer(PostActions.CREATE_POST_TYPES);

const rootReducer = combineReducers({
    error,
    login,
    post
});

export default rootReducer;