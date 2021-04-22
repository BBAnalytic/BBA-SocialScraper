import React, { Component } from 'react'
import { Redirect } from 'react-router'

export default class LoginAuthenticate extends Component {
    render() {
        
        return(
            <div>
                {this.props.redirect}
            </div>
        )
    }
}
