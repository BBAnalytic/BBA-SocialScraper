import React, { Component } from 'react'
import './css/RegisterAccountPage.css'
import HomeButton from './HomeButton'
import { Link } from 'react-router-dom'

export default class RegisterAccount extends Component {
	constructor(props){
		super(props);
		this.state = {
			email: '',
			downloadLocation: '',
			approved: false,
			deleted: false,
			saved: false,
			scrapeHistoryToggle: false,
			advancedSearchToggle: false,
			emailNotifToggle: false,
			title: "Create Your Account"
		};

		const emailRegex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}$$/;

		this.handleApproved = this.handleApproved.bind(this);
		this.handleDeleted = this.handleDeleted.bind(this);
		this.handleSaved = this.handleSaved.bind(this);
		this.handleScrapeTog = this.handleScrapeTog.bind(this);
		this.handleSearchTog = this.handleSearchTog.bind(this);
		this.handleNotifTog = this.handleNotifTog.bind(this);
	}

	handleApproved(event){

	}
	handleDeleted(event){

	}
	handleNotifTog(event){

	}
	handleSaved(event){

	}
	handleScrapeTog(event){

	}
	handleSearchTog(event){

	}

	render(){
		return(
			<div className="registerAccountPageContent">
				<div className="registerAccountPageTitleContainer">
					<label className="registerAccountPageTitle">
						Create Your Account
					</label>
				</div>

				<div className="settingsPageContainer">
					<div className="homeButtonContainer">
						<HomeButton></HomeButton>
					</div>

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
						
						<div className="createAccountButtonContainer">
							<button className="createAccountButton">Create Account</button>
						</div>
					</div>
				</div>

			</div>
		)
	}
}