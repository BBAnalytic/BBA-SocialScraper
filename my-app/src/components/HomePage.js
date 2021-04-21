import React, { Component } from 'react'
import SettingsButton from './SettingsButton'
import './css/HomePage.css'
import { Link, Redirect } from 'react-router-dom'
import NavButtons from './NavButtons'

export default class HomePage extends Component {
    constructor(props){
        super(props);
        this.state = {
            scrapeHistory: []
        };
    }

    componentDidMount(){
        const fetchURL = '/api/getRecentSearches';
        const fetchContent = {
            method: 'POST',
            body: JSON.stringify({
                email: this.props.email
            })
        }

        fetch(fetchURL, fetchContent)
            .then(response => response.json())
            .then(data => {
                console.log(data)
                console.log(data[0])
                console.log(data[0].s_platform)
                this.setState({
                    scrapeHistory: data
                })
            })
    }

    render() {
        if (this.props.email != ""){
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
                            <div className="scrapeHistoryContainer">
                                <div className="scrapeHistoryTitleContainer">
                                    <label>Scrape History</label>
                                </div>
                                <div className="scrapeHistoryButtonContainer">
                                    <div className="scrapeHistoryButtonOne">
                                        <button>{ this.state.scrapeHistory[0].s_platform }</button>
                                    </div>
                                </div>
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
        else{
            return (
                <Redirect to='/LoginPage'></Redirect>
            )
        }
    }
}
