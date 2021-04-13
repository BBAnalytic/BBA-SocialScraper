import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import './css/RegisterAccountConfirm.css'

export default class RegisterAccountConfirm extends Component {
	render() {
		return (
			<div className="registerAccountConPageContent">
				<div className="registerAccountConPageTitleContainer">
					<label className="registerAccountConPageTitle">
						Account Processing
					</label>
				</div>

				<div className="registerAccountConPageContainer">
					<div className="registerConfirmationTextContainer">
						<text className="txt-registerConfirmation">Your account has been successfully requested! <br />
						You must wait for a professor to approve your account privileges. Please check back within 48 hours,
						or check your email for a confirmation saying that you are approved/disapproved.
						</text>
					</div>
					<div className="returnHomeButtonContainer">
						<Link to="/LoginPage">
							<button className="btn-returnHomePage">Return to Login</button>
						</Link>
					</div>
				</div>


			</div>
		)
	}
}
