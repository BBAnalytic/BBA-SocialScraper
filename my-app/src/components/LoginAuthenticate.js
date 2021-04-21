import React, { Component } from 'react'
import { Redirect } from 'react-router'

export default class LoginAuthenticate extends Component {
    render() {
        
        console.log(this.props.isAuthenticated)
        return(
            <div>
                {this.props.redirect}
            </div>
        )
    }
}
