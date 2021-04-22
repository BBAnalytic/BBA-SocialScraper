import React, { Component } from 'react'
import { Redirect } from 'react-router'

export default class SettingsAuthenticate extends Component {
    render() {
        console.log(this.props.userAdmin);
        console.log("We go to SettingsAuth");
        if(this.props.userAdmin == true){
            return (
                <div>
                    <Redirect to='AdminSettingsPage'></Redirect>
                </div>
            )
        }
        else{
            return (
                <div>
                    <Redirect to='SettingsPage'></Redirect>
                </div>
            )
        }
    }
}
