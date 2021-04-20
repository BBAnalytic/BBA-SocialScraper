import React, { Component } from 'react'
import { Redirect } from 'react-router'

export default class LoginAuthenticate extends Component {
    constructor(props){
        super(props);
        this.state={
            isAuthenticated: false
        };

    }
    handleAuthentication(){
        if(this.state.isAuthenticated){
            return true;
        }
        else{
            return false;
        }
    }
    render() {
        console.log("LoginAuthenticating...")
        const fetchUrl = '/api/authenticateLogin';
        let isAuthenticatedVar = false;
        fetch(fetchUrl, {
            method: 'POST',
            body: JSON.stringify({
                email: this.props.email,
                password: this.props.password
            })
        })
        .then((response) => response.json())
        .then((data) => {
            if(data.result === 'OK Email/Password Validated'){
                this.setState({
                    isAuthenticated: true
                })
            }
        })
        if (this.handleAuthentication){
            return(
                <div>
                    <Redirect to='/HomePage'></Redirect>
                </div>
            )
        }
        else{
            return (
                <div>
                    <Redirect to='/LoginPage'></Redirect>
                </div>
            )
        }
    }
}
