import React, { Component } from 'react'
import './css/SettingsButton.css'
import settingsIcon from './settingsIcon.svg'
import { Link } from 'react-router-dom'

export default class SettingsButton extends Component {
    
    render() {
        return (
            <div className="navButtonContainer">
                <Link to='/HomePage'>
                    <button className="homeButton">
                        Home
                    </button>
                </Link>
            <Link to='/SettingsAuthenticate' className="settingsButtonContainer">
                <button className="settingsButton">
                    <text className="settingsButtonText">Settings</text>
                    <img src={settingsIcon} className="settingsIcon" />
                </button>
            </Link>
            </div>
        )
    }
}
