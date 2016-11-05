/**
 * Created by comyn on 16-11-5.
 */
import React from 'react';
import history from 'react-router/lib/browserHistory';
import connect from 'react-redux/lib/components/connect';
import autobind from 'core-decorators/lib/autobind';
import {STATUS_REQUEST, STATUS_SUCCESS, cleanToken, setToken} from '../middleware/fetch';
import * as UserAction from '../actions/user';

@connect(state => ({loginResult: state.login}), {login: UserAction.login})
export default class Login extends React.Component {
    constructor(props) {
        super(props);
        this.state = {mail: '', password: ''};
        cleanToken()
    }
    
    @autobind
    handleLogin() {
        this.props.login(this.state.mail, this.state.password)
    }

    componentWillReceiveProps(props) {
        if (props.loginResult.id !== this.props.loginResult.id) {
            if (props.loginResult.status === STATUS_SUCCESS) {
                const token = props.loginResult.res.token;
                setToken(token);
                history.push('/');
            }
        }
        this.props = props;
    }
    
    render() {
        return (
            <div className="modal is-active">
                <div className="modal-background"></div>
                <div className="modal-content">
                    <div className="box">
                        <p className="control has-icon">
                            <input type="email" 
                                   className="input"
                                   placeholder="Email"
                                   onChange={e => this.setState({mail: e.target.value})}
                                   value={this.state.mail}/>
                            <i className="fa fa-envelope" />
                        </p>
                        <p className="control has-icon">
                            <input type="password"
                                   className="input"
                                   placeholder="password"
                                   onChange={e => this.setState({password: e.target.value})}
                                   value={this.state.password}/>
                            <i className="fa fa-key" />
                        </p>
                        <p className="control">
                            <button className="button is-primary" onClick={this.handleLogin}>Login</button>
                        </p>
                    </div>
                </div>
            </div>
        )
    }
}
