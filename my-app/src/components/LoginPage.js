import React, { Component } from 'react'
import './css/LoginPage.css'
import { Link, Redirect, withRouter, useHistory } from 'react-router-dom'

export default class LoginPage extends Component {
    constructor(props){
        super(props);
        this.state = {
            email: '',
            password: '',
            submitted: false,
            link: '/HomePage'
        };

        const emailRegex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}$$/;
    }

    render() {
        return (
        
        <div className="loginPageContent">
            <div className="loginPageTitleContainer">
                <label className="loginPageTitle">
                    {this.props.title}
                </label>
            </div>
            <div className="loginPageContainer">
                <div className="contactUsContainer">
                    <Link to='/ContactUsPage'>
                        <button className="contactUsButton">Contact Us</button>
                    </Link>
                </div>
                <div className="loginFormContainer">
                    <form className="loginForm">
                        <input type="email" value={this.props.email} required placeholder="Email" onChange={this.props.handleEmailChange} className="emailInputBox" />
                        <input type="password" value={this.props.password} placeholder="Password" onChange={this.props.handlePasswordChange} className="passwordInputBox" />
                        <input type="button" value="Forgot Password" className="forgotPasswordButton" />
                        <Link to='/LoginAuthenticate'>
                            <input type="submit" value="Login" className="loginButton" />
                        </Link>
                    </form>
                </div>
                <Link to='/RegisterAccount' className="createContainer">
                    <button className="createButton">Create</button>
                </Link>
            </div>
        </div>
        )
    }
}
