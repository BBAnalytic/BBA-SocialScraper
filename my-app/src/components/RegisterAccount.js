import React, { Component } from 'react'
import './css/RegisterAccountPage.css'
import HomeButton from './HomeButton'
import { Link } from 'react-router-dom'

export default class RegisterAccount extends Component {
	constructor(props){
		super(props);
		this.state = {
			email: '',
			name: '',
			password: '',
			passCon: '',
			title: "Create Your Account"
		};

		const emailRegex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}$$/;

		this.handleCreateAccount = this.handleCreateAccount.bind(this);
	}

	handleCreateAccount(){
		let email = document.getElementById("s_emailInput").value;
		let name = document.getElementById("s_nameInput").value;
		let pass = document.getElementById("s_passInput").value;
		let passConfirm = document.getElementById("s_pass2Input").value;

		if(!email || !name || !pass || !passConfirm){
			window.alert("Please fill out all the fields.");
		}
		else{
			<Link to='/RegisterAccountConfirm'></Link>
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
									<input type="text" id="s_nameInput" className="nameInputBoxR" placeHolder="First M. Last"></input>
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
							<button className="createAccountButton" onClick={this.handleCreateAccount}>Create Account</button>
						</div>
					</div>
				</div>
			</div>
		)
	}
}