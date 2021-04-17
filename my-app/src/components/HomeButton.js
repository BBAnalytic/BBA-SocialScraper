import React, { Component } from 'react'
import './css/HomeButton.css'
import settingsIcon from './homeIcon.svg'
import { NavLink, Redirect, Router } from 'react-router-dom'

export default class HomeButton extends Component {
    render() {
        return (
            <NavLink to='/HomePage' className="homeButtonContainer">
                <button className="homeButton">
                    {/* <img src={settingsIcon} className="homeIcon" /> */}
                </button>
            </NavLink>
        )
    }
}
