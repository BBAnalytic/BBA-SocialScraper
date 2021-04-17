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
			json: {},
			allAccounts: [],
			usersLoaded: false,
			title: 'Admin Settings',
			link: '/LoginPage'
		};

		const emailRegex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}$$/;

		this.handleApproved = this.handleLogout.bind(this);
		this.handleGetUsers = this.handleGetUsers.bind(this);
		this.createList = this.createList.bind(this);
	}

	handleLogout(event){
		
	}

	handleAlert(event){
		window.alert("test");
	}

	//createList takes the json data and turns it into a list format with the necessary className tags for styling
	createList = () => {
		let accounts = [];

		for(let i = 0; i < this.state.json.length; i++){
			let children = [];
			for(let j = 0; j < 1; j++){
				children.push(<div><li className="accountInScrollBox">{this.state.json[0].s_email}</li></div>)
			}
			accounts.push(<div className="accountInScrollBoxContainer">{children}</div>)
		}
		return accounts;
	}


	// to access data in the json file in react:
	// .then(data => response.json())
	// .then(data => {
		// console.log(data[0].s_email);
		// console.log(data[1].s_email);
	// })
	//this will grab each one, just replace the array numbers and the s_email with wanted values
	handleGetUsers(event){
		//fetch from the endpoint getAllAccounts, take in json data
		fetch('/api/getAllAccounts')
			.then(res => res.json())
			.then(result => {
				console.log("First: ", result[0].s_first);
				this.setState({
					usersLoaded: true,				//to let the scroll box area to know to start rendering the data
					json: result					//to store the actual json data as a prop
				})
				console.log("Data Stuff: ", this.state.json[1].s_first);
				
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



	render (){
		return(
			<div className="adminSettingsPageContent">
				<div className="settingsPageTitleContainer">
					<text className="adminSettingsPageTitle">
						{this.props.title}
					</text>
				</div>

				{/* These buttons are for testing the endpoints */}
				<div className="btn-testPurposes">
					<button onClick={() => {this.handleGetUsers()}}>Get Users</button>
					{/* <button onClick={() => {this.handleDeleteUser()}}>Delete User</button> */}
					{/* have to use email to change user, so need to set the email to the
					classname bc the only thing that's displayed is username */}
					{/* <button onClick={this.handleApproveUser}>Approve User</button>
					<button onClick={this.handleBanUser}>Ban User</button>
					<button onClick={this.handleAlert}>Alert Time</button> */}
				</div>

				<div className="settingsPageContainer">
					<HomeButton className="homeButtonAdmin"></HomeButton>
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
									<div className="topButtonsContainer">
										<button className="btn-saveChanges">Save Changes</button>
									</div>
								</div>
							</form>
						</div>
					</div>
					<div className="approveAccountsContainer">
						<div className="approveAccountsTitleContainer">
							<text className="approveAccountsTitle">Approve Accounts</text >
						</div>
						<div className="approveScrollingContainer">
							<div className="approveScrollBox">
								{/* {console.log("Handle Users: ", this.handleGetUsers())} */}
								{/* <button onClick={() => {console.log("Handle Users: ", this.handleGetUsers())}}>Get Users</button> */}
								
								{this.state.usersLoaded ? this.createList() : console.log('No data.')}

								{/* Test foreach loop to iterate */}
								
								{/* {this.state.json.map(person => (
									<li>{person.s_email}</li>
								))} */}
								
								
								{/* {this.state.usersLoaded && <h1>'Changed successfully.'</h1>} */}


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
								<button className="deactivateAccountButton">Deactivate Account</button>
							</Link>
						</div>
					</div>
				</div>
			</div>
		)
	}
}