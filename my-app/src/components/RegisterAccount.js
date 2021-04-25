import React, { Component } from 'react'
import './css/RegisterAccountPage.css'
import HomeButton from './HomeButton'
import { Link } from 'react-router-dom'
import { Redirect } from 'react-router-dom'

export default class RegisterAccount extends Component {
	constructor(props){
		super(props);
		this.state = {
			title: "Register Your Account"
		};

		const emailRegex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}$$/;

		this.handleCreateAccount = this.handleCreateAccount.bind(this);
	}

	//handleCreateAccount grabs whatever is currently typed in the input fields
	//and checks to make sure the data is reasonable. (TODO: more of that, check email syntax)
	//it takes no arguments and returns nothing.
	handleCreateAccount(){
		let email = document.getElementById("s_emailInput").value;
		let name = document.getElementById("s_nameInput").value;
		let pass = document.getElementById("s_passInput").value;
		let passConfirm = document.getElementById("s_pass2Input").value;

		if(email && name && pass && passConfirm){
			if(pass == passConfirm){
				const requestOptions = {
					method: 'POST',
					headers: { 'Content-Type': 'applications/json'},
					body: JSON.stringify({ "email": email, "name": name, "password": pass})
				}
		
				fetch('/api/createUser', requestOptions)
					.then(data => {
						//TODO: check that the action was successful, assuming that it is rn
					});
			}
		}
	}

	render(){
		return(
			<div className="registerAccountPageContent">
				<div className="registerAccountPageTitleContainer">
					<label className="registerAccountPageTitle">
						{this.state.title}
					</label>
				</div>

				<div className="registerAccountPageContainer">
					<div className="emailDownloadContainer">
						<form className="emailDownloadForm">
							<div className="formContainer">
								<div className="emailContainerR">
									<label className="emailTextR">Email: </label>
									<input type="email" id="s_emailInput" className="emailInputBoxR" placeholder="first.last@email.com"></input>
								</div>
								<div className="nameContainer">
									<label className="nameText">Name: </label>
									<input type="text" id="s_nameInput" className="emailInputBoxR" placeHolder="First Last"></input>
								</div>
								<div className="passwordContainer">
									<label className="passwordText">Password: </label>
									<input type="password" id="s_passInput" className="passwordInputBox" placeHolder="*********"></input>
								</div>
								<div className="passwordConfirmContainer">
									<label className="passwordConfirmText">Re-type Password: </label>
									<input type="password" id="s_pass2Input" className="passwordConfirmInputBox" placeHolder="*********"></input>
								</div>
							</div>
						</form>
						
						<div className="returnToLoginBtnContainer">
							<Link to='/LoginPage'>
								<button className="btn-returnToLoginPage">Return to Login</button>
							</Link>
						</div>

						<div className="createAccountButtonContainer">
						<Link to="/RegisterAccountConfirm">
							<button className="createAccountButton" onClick={this.handleCreateAccount}>Create Account</button>
							</Link>
						</div>
					</div>
				</div>
			</div>
		)
	}
}