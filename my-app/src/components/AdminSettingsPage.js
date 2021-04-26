import React, { Component } from 'react'
import { Link, Redirect } from 'react-router-dom';
import SettingsButton from './SettingsButton';
import './css/AdminSettingsPage.css'
import { confirmAlert } from 'react-confirm-alert'; 
import 'react-confirm-alert/src/react-confirm-alert.css'

export default class AdminSettingsPage extends Component {
	constructor(props){
		super(props);
		this.state = {
			json: {},
			pageLoad: true,			//false when it's not meant to load, true when it's meant to load. starts at true so that it can initially load.
			usersLoaded: false,		//false when the users haven't been fetched yet, is set to true when ready to display the fetched accounts
			title: 'Admin Settings'
		};

		this.handleApproved = this.handleLogout.bind(this);
		this.handleGetUsers = this.handleGetUsers.bind(this);
		this.createList = this.createList.bind(this);
		this.handleDeleteUser = this.handleDeleteUser.bind(this);
	}

	handleLogout(event){
		
	}

	//createList fetches the json data and loops over each account in the database
	//with each account, four buttons are created: Approve, Admin, Delete, and Ban
	//each button is connected onclick to its respective function above
	//when styling CSS, keep the containers around each button directly on each button, otherwise clickability will be affected
	//RETURNS: accounts, an array variable that has all of the account information and labels for styling (as shown below)
	createList = () => {
		let accounts = [];

		for(let i = 0; i < this.state.json.length; i++){
			let children = [];
			for(let j = 0; j < 1; j++){
				const s_tempEmail = this.state.json[i].s_email;
				children.push(
					<div className="accountInScrollBoxContainer">
						<div className="nameContainer">
							<li className="accountInScrollBox">{this.state.json[i].s_first_name} {this.state.json[i].s_last_name} {this.state.json[i].b_banned && "[Banned]"} {this.state.json[i].b_admin && "[Admin]"} {!this.state.json[i].b_approved && "[Pending]"}</li>
						</div>
						<div className="emailContainer">
							<li className="emailInScrollBox">{this.state.json[i].s_email}</li>
						</div>
						<div className="btn-containersAccounts">
							<div className="btn-approveContainer">
								{!this.state.json[i].b_approved && <button className="btn-approve" onClick={() => this.handleApproveUser(this.state.json[i].s_email)}>Approve</button>}
							</div>
							<div className="btn-adminContainer">
								{!this.state.json[i].b_admin && !this.state.json[i].b_banned && <button className="btn-admin" onClick={() => this.handleAdminUser(s_tempEmail, true)}>Admin</button>}
							</div>
							<div className="btn-deleteContainer">
								<button className="btn-delete" onClick={() => this.deleteUserAlert(s_tempEmail)}>Delete</button>
							</div>
							<div className="btn-banContainer">
								{!this.state.json[i].b_banned && <button className="btn-banUser" onClick={() => this.handleBanUser(s_tempEmail, true)}>Ban</button>}
							</div>
						</div>
					</div>
				)
			}
			accounts.push(<div className="containerOfAllScrollChildren">{children}</div>)
		}
		return accounts;
	}

	//handleGetUsers takes no arguments
	//it fetches the data from the endpoint getAllAccounts, which gives all the accounts in the database.
	//It returns nothing, but sets a prop named json to the result from the fetch
	handleGetUsers(){
		//fetch from the endpoint getAllAccounts, take in json data
		fetch('/api/getAllAccounts')
			.then(res => res.json())
			.then(result => {
				this.setState({
					pageLoad: false,				//to tell the page that it's not time to reload
					usersLoaded: true,				//to let the scroll box area to know to start rendering the data
					json: result					//to store the actual json data as a prop
				})
		});
	}

	//handleApproveUser takes one argument: email, which is the user's email address for database use
	//it posts to the endpoint setApprove, sending the email address
	//this approves the user and marks their approval in the database to true
	//handleApproveUser returns nothing
	handleApproveUser(email){
		const requestOptions = {
			method: 'POST',
			headers: { 'Content-Type': 'applications/json'},
			body: JSON.stringify({"s_user_email": email,"b_approve_value": true})
		}

		fetch('/api/setApprove', requestOptions)
			.then(data => {
				this.setState({
					pageLoad: true
				})
				
			})
	}


	handleAdminUser(email, isAdmin){
		this.handleApproveUser(email);

		const requestOptions = {
			method: 'POST',
			headers: { 'Content-Type': 'applications/json'},
			body: JSON.stringify({ "s_user_email": email, "b_admin_value": isAdmin})
		}

		fetch('/api/setAdmin', requestOptions)
			.then(data => {
				this.setState({
					pageLoad: true						//tell the page it's time to stop
				})
			});
	}

	deleteUserAlert(email){
		confirmAlert({
			title: 'Confirm Deletion',
			message: 'Are you sure you want to delete '+ email + '\'s account?',
			buttons: [
			  {
				label: 'Yes',
				onClick: () => {this.handleDeleteUser(email)}
			  },
			  {
				label: 'No',
				onClick: () => {return false}
			  }
			]
		  })
	}

	handleDeleteUser(email){
		const requestOptions = {
			method: 'POST',
			headers: { 'Content-Type': 'applications/json'},
			body: JSON.stringify({ "email": email })
		}

		fetch('/api/deleteUser', requestOptions)
			.then(data => {
				this.setState({
					pageLoad: true						//tell the page it's time to stop
				})
				// TODO: get the confirmation and error check
			});
	}

	handleBanUser(email, isBanned){
		this.handleAdminUser(email, false);

		const requestOptions = {
			method: 'POST',
			headers: { 'Content-Type': 'applications/json'},
			body: JSON.stringify({"s_user_email": email,"b_ban_value": isBanned})
		}

		fetch('/api/setBan', requestOptions)
			.then(data => {
				this.setState({
					pageLoad: true
				})
				// TODO: get the confirmation and error check
			})
	}

	render (){
		if(this.props.email != ""){

			return(
				<div className="adminSettingsPageContent">
					<div className="settingsPageTitleContainer">
						<text className="adminSettingsPageTitle">
							{this.state.title}
						</text>
					</div>
	
					<div className="settingsPageContainer">
						<SettingsButton className="settingsButtonAdmin"></SettingsButton>
						<div className="secondRowContainer">
							<div className="emailDownloadContainer">
								<form className="emailDownloadForm">
									<div className="formContainer">
										<div className="emailContainerS">
											<text className="emailTextS">Email: {this.props.email}</text>
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
	
									{this.state.pageLoad && this.handleGetUsers()}
									{this.state.usersLoaded && this.createList()}
	
								</div>
							</div>
						</div>
						<div className="bottomButtonsContainerA">
							<div className="logoutButtonContainer">
							<Link to='/LoginPage'>
								<button className="logoutButton" onClick={this.handleLogout}>Logout</button>
							</Link>
							</div>
							<div className="btn-deactivateContainer">
								<Link to='/LoginPage'>
									<button className="deactivateAccountButton" onClick={() => this.handleDeleteUser(this.props.email)}>Deactivate Account</button>
								</Link>
							</div>
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