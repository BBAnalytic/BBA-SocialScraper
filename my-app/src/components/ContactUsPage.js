import React, { Component } from 'react'
import './css/ContactUsPage.css'
import { Link } from 'react-router-dom'

export default class ContactUsPage extends Component {
	constructor(props){
        super(props);
        this.state = {
            title: 'Contact Us Form'
        };

        const emailRegex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}$$/;

		this.handleSubmit = this.handleSubmit.bind(this);
    }

	handleSubmit(event){
		let email = document.getElementById("s_email").value;
		let message = document.getElementById("s_message").value;

		if(message.length > 500){
			window.alert("Please use only 500 or less characters. You are at ", message.length, " characters now.");
		}
	}
	
	render() {
		return (
			<div className="contactUsPageContent">
				<div className="contactUsPageTitleContainer">
					<label className="contactUsPageTitle">
						{this.state.title}
					</label>
				</div>

				<div className="contactUsPageContainer">
					<div className="emailContainer">
						<div className="emailLabelContainerC">
							<text className="emailTextC">
								Your Email:
							</text>
						</div>
						<div className="emailInputContainer">
							<input type="email" id="s_email" placeholder="Email" value={this.state.email} required requirederror="Email Address required." validate={this.emailRegex} validateerror="Please provide a valid email address." placeholder="Email" onChange={this.handleEmailChange} className="emailInputBox"></input>
						</div>
					</div>
					<div className="messageContainer">
						<div className="messageLabelContainer">
							<text className="messageText">
								Message:
							</text>
							</div>
						<div className="messageInputContainer">
							<textarea placeholder="Message" id="s_message" className = "messageInputBox" name="text" rows="1" cols="1" wrap="soft"></textarea>
						</div>
					</div>
					<div className="buttonContainer">
						<Link to='/LoginPage'>
							<button className="goBackButton">Go Back</button>
						</Link>
						<Link to='/ContactUsConfirmationPage'>
							<button className="submitButton">Submit</button>
						</Link>
					</div>
				</div>
			</div>
        )
	}
}
