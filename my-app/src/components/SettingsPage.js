import React, { Component } from 'react'
import './css/SettingsPage.css'
import HomeButton from './HomeButton'
import { Link, Redirect } from 'react-router-dom'

export default class SettingsPage extends Component {
	constructor(props){
		super(props);
		this.state = {
			email: ''
		};

		this.handleDeleteUser = this.handleDeleteUser.bind(this);
	}

	handleDeleteUser(email){
		const requestOptions = {
			method: 'POST',
			headers: { 'Content-Type': 'applications/json'},
			body: JSON.stringify({ "email": this.props.email })
		}

		fetch('/api/deleteUser', requestOptions)
			.then(data => {
				console.log('deleted');
				// TODO: get the confirmation and error check
			});
	}

	render(){
		if(this.props.email != ""){
			return(
				<div className="settingsPageContentS">
					<div className="settingsPageTitleContainerS">
						<label className="settingsPageTitleS">
							{this.props.title}
						</label>
					</div>
					{/* TODO: add home page button */}

					<div className="settingsPageContainerS">
						<div className="secondRowContainer">
							<div className="emailDownloadContainerS">
								<form className="emailDownloadForm">
									<div className="formContainer">
										<div className="emailContainerS">
											<label className="emailTextS">Email: {this.props.email}</label>
										</div>
									</div>
								</form>
							</div>
						</div>
						
						<div className="bottomButtonsContainerS">
							<Link to='/LoginPage' className="logoutButtonContainerS">
								<button className="logoutButton">Logout</button>
							</Link>
							<Link to='/LoginPage' className="topButtonsContainerS">
								<button className="deactivateAccountButton" onClick={() => this.handleDeleteUser()}>Deactivate Account</button>
							</Link>
						</div>
					</div>
				</div>
			)
		}
		else{
			return(
				<div>
					<Redirect to='/LoginPage'></Redirect>
				</div>
			)
		}
	}
}