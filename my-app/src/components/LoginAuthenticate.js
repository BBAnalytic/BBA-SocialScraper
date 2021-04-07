import React, { Component } from 'react'
import { Redirect } from 'react-router'

export default class LoginAuthenticate extends Component {
    constructor(props){
        super(props);
        this.state={
            isAuthenticated: false
        };
    }
    
    render() {
        console.log("LoginAuthenticating...")
        const fetchUrl = '/api/loginUser/';
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
                // this.setState({isAuthenticated: true});
                // console.log(this.state.isAuthenticated)
                let isAuthenticatedVar = true;
                console.log("Attempting to LOGIN")
                return (
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
        })
        // if (isAuthenticatedVar){
            
        // }
        // else{
        //     console.log("Login Failed: " + isAuthenticatedVar)
        //     return (
        //         <div>
        //             <Redirect to='/LoginPage'></Redirect>
        //         </div>
        //     )
        // }
    }
}
