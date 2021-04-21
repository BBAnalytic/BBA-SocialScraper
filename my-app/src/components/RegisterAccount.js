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

	handleCreateAccount(email, name, pass, passConfirm){
		if(pass == passConfirm){

		}
		else{
			window.alert("The passwords do not match.")
		}
	}

	updateEmailInput(email){

	}
	updateNameInput(name){

	}
	updatePasswordInput(pass){
		
	}
	updatePassCon(passCon){

	}


	render(){
		return(
			<div className="registerAccountPageContent">
				<div className="registerAccountPageTitleContainer">
					<label className="registerAccountPageTitle">
						Create Your Account
					</label>
				</div>

				<div className="registerAccountPageContainer">
					<div className="emailDownloadContainer">
						<form className="emailDownloadForm">
							<div className="formContainer">
								<div className="emailContainerR">
									<label className="emailTextR">Email: </label>
									<input type="email" className="emailInputBoxR" placeholder="first.last@email.com"></input>
								</div>
								<div className="nameContainer">
									<label className="nameText">Name: </label>
									<input type="text" className="nameInputBoxR" placeHolder="First M. Last"></input>
								</div>
								<div className="passwordContainer">
									<label className="passwordText">Password: </label>
									<input type="password" className="passwordInputBox" placeHolder="*********"></input>
								</div>
								<div className="passwordConfirmContainer">
									<label className="passwordConfirmText">Re-type Password: </label>
									<input type="password" className="passwordConfirmInputBox" placeHolder="*********"></input>
								</div>
							</div>
						</form>
						
						<div className="returnToLoginBtnContainer">
							<Link to='/LoginPage'>
								<button className="btn-returnToLoginPage">Return to Login</button>
							</Link>
						</div>

						<div className="createAccountButtonContainer">
							<Link to='/RegisterAccountConfirm'>
								<button className="createAccountButton" onClick={this.handleCreateAccount()}>Create Account</button>
							</Link>
						</div>
					</div>
				</div>
			</div>
		)
	}
}