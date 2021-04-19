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
			pageLoad: true,
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
				children.push(
					<div className="accountInScrollBoxContainer">
						<li className="accountInScrollBox">{this.state.json[i].s_first_name} {this.state.json[i].s_last_name}</li>
						<li className="emailInScrollBox">{this.state.json[i].s_email}</li>
					</div>
				)
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
				this.setState({
					pageLoad: false,
					usersLoaded: true,				//to let the scroll box area to know to start rendering the data
					json: result					//to store the actual json data as a prop
				})
		});
	}

	handleAdminUser(email){

	}

	handleDeleteUser(email){
		const requestOptions = {
			method: 'POST',
			headers: { 'Content-Type': 'applications/json'},
			body: JSON.stringify({ "email": email })
		}

		console.log("jsonsstuff: ", JSON.stringify({ 'email': email }));
		fetch('/api/deleteUser', requestOptions)
			// .then(res => res.json())
			.then(data => {
				if(!data.ok){
					throw 'Error';
				}
				else{
					console.log("Deleted user result: ", data);
				}
			});
	}

	handleApproveUser(email){

	}

	handleBanUser(email){

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

				<div className="settingsPageContainer">
					<HomeButton className="homeButtonAdmin"></HomeButton>
					<div className="secondRowContainer">
						<div className="emailDownloadContainer">
							<form className="emailDownloadForm">
								<div className="formContainer">
									<div className="emailContainerS">
										<text className="emailTextS">Email: </text>
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
								{/* {!this.state.json[i].b_approved && <button className="btn-approve" onClick={() => this.handleApproveUser(this.state.json[i].s_email)}>Approve</button>} */}
								{/* <button className="btn-admin" onClick={() => this.handleAdminUser(this.state.json[i].s_email)}>Admin</button> */}
								{/* <button className="btn-banUser" onClick={() => this.handleBanUser(this.state.json[i].s_email)}>Ban</button> */}
								<button className="btn-delete" onClick={() => this.handleDeleteUser('test@gmail.com')}>Delete</button>
							 	

								{/* The two following lines are what grab the accounts from the database (calling handleGetUsers()) and display the list (createList)  */}
								{this.state.pageLoad && 
									this.handleGetUsers()
								}
								{this.state.usersLoaded ? this.createList() : console.log('No data.')}
								
								{/* get the length of the json data (number of accounts returned) */}
								{/* make a loop for that amount of data?? send out the buttons */}

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