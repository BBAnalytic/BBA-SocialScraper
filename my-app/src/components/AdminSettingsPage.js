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
			pageLoad: true,			//false when it's not meant to load, true when it's meant to load. starts at true so that it can initially load.
			usersLoaded: false,
			title: 'Admin Settings',
			link: '/LoginPage'
		};

		const emailRegex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}$$/;

		this.handleApproved = this.handleLogout.bind(this);
		this.handleGetUsers = this.handleGetUsers.bind(this);
		this.createList = this.createList.bind(this);
		this.handleDeleteUser = this.handleDeleteUser.bind(this);
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
								<button className="btn-delete" onClick={() => this.handleDeleteUser(s_tempEmail)}>Delete</button>
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
					pageLoad: false,				//to tell the page that it's not time to reload
					usersLoaded: true,				//to let the scroll box area to know to start rendering the data
					json: result					//to store the actual json data as a prop
				})
		});
	}

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
				// TODO: get the confirmation and error check
			})
	}

	handleAdminUser(email, isAdmin){
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
				// TODO: get the confirmation and error check
			});
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
								{/* The two following lines are what grab the accounts from the database (calling handleGetUsers()) and display the list (createList)  */}
								{this.state.pageLoad ? this.handleGetUsers() : console.log("Cannot reload.")}
								{this.state.usersLoaded ? this.createList() : console.log('No data.')}

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
								<button className="deactivateAccountButton">Deactivate Account</button>
							</Link>
						</div>
					</div>
				</div>
			</div>
		)
	}
}