import React from 'react';
import 'bulma/bulma.sass';

export default class App extends React.Component {
    render() {
        return (
            <div>{this.props.children}</div>
        )
    }
}