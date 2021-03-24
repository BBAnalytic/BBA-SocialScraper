import React, { Component } from 'react'
import SettingsButton from './SettingsButton'
import './css/HomePage.css'
import { Link } from 'react-router-dom'
import NavButtons from './NavButtons'

export default class HomePage extends Component {

    render() {
        return (
            <div className="homePageContent">
                <div className="homePageTitleContainer">
                    <text className="homePageTitle">
                        {this.props.title}
                    </text>
                </div>
                <div className="homePageContainer">
                    
                <SettingsButton className="homeSettingsButton"></SettingsButton>
                    
                    <div className="homePageContentContainer">
                        <div className="previousSearchContainer">
                            Test
                        </div>
                        <div className="buttonContainer">
                            <Link to='/SearchCriteriaPage' className="newSearchContainer">
                                <button className="newSearchButton">
                                    New Search
                                </button>
                            </Link>
                            <div className="currentSearchesContainer">
                                <button className="currentSearchesButton">
                                    Current Searches
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}
