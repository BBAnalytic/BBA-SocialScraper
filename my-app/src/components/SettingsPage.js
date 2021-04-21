import React, { Component } from 'react'
import './css/SettingsPage.css'
import HomeButton from './HomeButton'
import { Link, Redirect } from 'react-router-dom'

export default class SettingsPage extends Component {
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
			emailNotifToggle: false
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
        if (this.props.email != ""){
			return(
				<div className="adminSettingsPageContent">
					<div className="settingsPageTitleContainer">
						<label className="contactUsPageTitle">
							{this.props.title}
						</label>
					</div>

					<div className="settingsPageContainer">
						<div className="homeButtonContainer">
							<HomeButton></HomeButton>
						</div>
						<div className="secondRowContainer">
							<div className="emailDownloadContainer">
								<form className="emailDownloadForm">
									<div className="formContainer">
										<div className="emailContainer">
											<label className="emailText">Email: </label>
											<input type="email" className="emailInputBox" placeholder="first.last@email.com"></input>
										</div>
										<div className="downloadContainer">
											<label className="downloadText">Download Location: </label>
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
						
						<div className="bottomButtonsContainer">
							<Link to='/LoginPage' className="logoutButtonContainer">
								<button className="logoutButton" onClick={ this.props.handleLogout }>Logout</button>
							</Link>
							<Link to='/LoginPage' className="topButtonsContainer">
								<button className="deactivateAccountButton">Deactivate Account</button>
							</Link>
						</div>
						<Link to='/HomePage' className="saveChangesButtonContainer">
							<button className="saveChangesButton">Save Changes</button>
						</Link>
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