import React, { Component } from 'react'
import { Link } from 'react-router-dom';
import HomeButton from './HomeButton';
import './css/SettingsPage.css'

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
	}

	handleLogout(event){

	}

	render(){
		return(
			<div className="adminSettingsPageContent">
				<div className="settingsPageTitleContainer">
					<text className="adminSettingsPageTitle">
						{this.props.title}
					</text>
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
						<div className="toggleButtonsContainer">
							<div className="scrapeHistoryToggleContainer">
								<button className="scrapeHistoryToggle">See Scrape History</button>
							</div>
							<div className="advancedSearchToggleContainer">
								<button className="advancedSearchToggle">Always Advanced Search</button>
							</div>
							<div className="emailNotifToggleContainer">
								<button className="emailNotifToggle">Email Notifications</button>
							</div>
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
						</div>
					</div>
					<div className="bottomButtonsContainer">
						<div className="logoutButtonContainer">
						<Link to='/LoginPage'>
							<button className="logoutButton" onClick={this.handleLogout}>Logout</button>
						</Link>
						</div>
						<div className="saveChangesButtonContainer">
							<button className="saveChangesButton">Save Changes</button>
						</div>
					</div>
				</div>
			</div>
		)
	}
}