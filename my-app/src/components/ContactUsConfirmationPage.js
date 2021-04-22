import React, { Component } from 'react'
import './css/ContactUsConfirmationPage.css'
import { Link } from 'react-router-dom'

export default class ContactUsConfirmationPage extends Component {
	constructor(props){
		super(props);
		this.state = {
			title: 'Contact Us Confirmation'
		};

		this.handleReturnToLogin = this.handleReturnToLogin.bind(this);
	}

	handleReturnToLogin(event){
		
	}



	render() {
		return (
			<div className="contactUsConfirmPageContent">
				<div className="conUsConPageTitleContainer">
					<label className="conUsConPageTitle">{this.props.title}</label>
				</div>

				<div className="conUsConContentContainer">
					<div className="conUsConTextContainer">
						<text className="conUsConText">Your message was successfully sent. Please wait approximately 2-4 business days for a reply to your email at
						socialscraper24@gmail.com.</text>
					</div>
					<div className="conUsConReturnButtonContainer">
						<Link to="/LoginPage">
							<button className="btn-returnToLogin">Return to Login</button>
						</Link>
					</div>
				</div>
			</div>
		)
	}
}
