import React, { Component } from 'react'
import { Link } from 'react-router-dom';
import HomeButton from './HomeButton';
import './css/AdminSettingsPage.css'

export default class AdminSettingsPage extends Component {
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
			title: 'Admin Settings',
			link: '/LoginPage'
		};

		const emailRegex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}$$/;

		this.handleApproved = this.handleLogout.bind(this);
		this.handleGetUsers = this.handleGetUsers.bind(this);
	}

	handleLogout(event){
		
	}

	handleGetUsers(event){
		// fetch('http://localhost:5000/api/getAllAccounts', {method: 'GET'}).then(data => console.log(data));
		fetch('/api/getAllAccounts')
			.then(response => response.json())
			.then(data => {
				console.log(data)
  		});
	}

	handleDeleteUser(event){
		const email = 'z@z.z';

		fetch('/api/deleteUser', {method: 'POST'},)
			.then()
			.then({

			});
	}

	handleApproveUser(event){

	}

	handleBanUser(event){

	}

	handleScrapeHistoryToggle(event){

	}


	render(){
		return(
			<div className="adminSettingsPageContent">
				<div className="settingsPageTitleContainer">
					<text className="adminSettingsPageTitle">
						{this.props.title}
					</text>
				</div>

				{/* These buttons are for testing the endpoints */}
				<div className="btn-testPurposes">
					<button onClick={this.handleGetUsers}>Get Users</button>
					<button onClick={this.handleDeleteUser}>Delete User</button>
					{/* have to use email to change user, so need to set the email to the
					classname bc the only thing that's displayed is username */}
					<button onClick={this.handleApproveUser}>Approve User</button>
					<button onClick={this.handleBanUser}>Ban User</button>
				</div>

				<div className="settingsPageContainer">
					<HomeButton className="homeButtonAdmin"></HomeButton>
					<div className="topButtonsContainer">
						<button className="contactRequestButton">View Contact Requests</button>
						<button className="editUsersButton">Edit Users</button>
						<button className="deactivateAccountButton">Deactivate Account</button>
					</div>
					<div className="secondRowContainer">
						<div className="emailDownloadContainer">
							<form className="emailDownloadForm">
								<div className="formContainer">
									<div className="emailContainerS">
										<text className="emailTextS">Email: </text>
										<input type="email" className="emailInputBoxS" placeholder="first.last@email.com"></input>
									</div>
									<div className="downloadContainer">
										<text className="downloadText">Download Location: </text>
										<input type="text" className="downloadLocationBox" placeholder="C:/Downloads"></input>
									</div>
								</div>
							</form>
						</div>
					</div>
					<div className="approveAccountsContainer">
						<div className="approveAccountsTitleContainer">
							<text className="approveAccountsTitle">Approve Accounts</text>
						</div>
						<div className="approveScrollingContainer">
							<div className="approveScrollBox">
								Scroll box: needs to be hooked up to DB.
								{/*needs to hook up to DB to show accounts to approve.*/}
							</div>
						</div>
						<div className="delAppButtonsContainer">
							<div className="deleteButtonContainer">
								<button className="deleteButton">Delete</button>
							</div>
							<div className="approveButtonContainer">
								<button className="approveButton">Approve</button>
							</div>
							<div className="banButtonContainer">
								<button className="btn-ban">Ban</button>
							</div>
						</div>
					</div>
					<div className="bottomButtonsContainerA">
						<div className="logoutButtonContainer">
						<Link to='/LoginPage'>
							<button className="logoutButton" onClick={this.handleLogout}>Logout</button>
						</Link>
						</div>
						<div className="saveChangesButtonContainerA">
							<Link to='/LoginPage'>
								<button className="btn-saveChanges">Save Changes</button>
							</Link>
						</div>
					</div>
				</div>
			</div>
		)
	}
}