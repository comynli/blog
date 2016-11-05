/**
 * Created by comyn on 16-11-5.
 */
import React from 'react';
import marked from 'marked';
import history from 'react-router/lib/browserHistory';
import connect from 'react-redux/lib/components/connect';
import autobind from 'core-decorators/lib/autobind';
import {STATUS_REQUEST, STATUS_SUCCESS} from '../middleware/fetch';
import * as PostAction from '../actions/post';


@connect(state => ({post: state.post}), {create: PostAction.create})
export default class Editor extends React.Component {
    constructor(props) {
        super(props);
        this.props.create(1);
        this.state = {code: ''}
    }
    
    render() {
        return (
            <div className="columns">
                <div className="column">
                    <textarea value={this.state.code} onChange={e => this.setState({code: e.target.value})}/>
                </div>
                <div className="column" dangerouslySetInnerHTML={{__html:marked(this.state.code, {sanitize: true})}}>
                    
                </div>
            </div>
        )
    }
}
