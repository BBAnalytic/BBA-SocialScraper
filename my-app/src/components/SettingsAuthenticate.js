import React, { Component } from 'react'
import { Redirect } from 'react-router'

export default class SettingsAuthenticate extends Component {
    render() {
        if(this.props.userAdmin == true){
            return (
                <div>
                    <Redirect to='/AdminSettingsPage'></Redirect>
                </div>
            )
        }
        else{
            return (
                <div>
                    <Redirect to='/SettingsPage'></Redirect>
                </div>
            )
        }
    }
}
