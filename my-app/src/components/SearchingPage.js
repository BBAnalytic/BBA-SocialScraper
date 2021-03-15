/*
* Name: James West
* Date Created: 03/05/2021
* Version: 1.0
* Description: The page that shows the details of a specific scrape that is currently being run.
*/

import React, { Component } from 'react'
import SearchingDataContent from './SearchingDataContent';
import SettingsButton from './SettingsButton';
import './css/SearchingPage.css'
import { Link } from 'react-router-dom';

export default class SearchingPage extends Component {
    constructor(props){
        super(props);
        this.state = {
            scraped: '3200'  // Number of units that the API has scraped
        }
        
        this.handleScrapeUpdate = this.handleScrapeUpdate.bind(this);
        this.handleEndSearch = this.handleEndSearch.bind(this);
        this.handleNewSearch = this.handleNewSearch.bind(this);
    };

    handleScrapeUpdate(){
        // Ever X seconds update
        const fetchUrl = '/api/scrapeCount/';

        fetch(fetchUrl, {
            method: 'GET',
            body: JSON.stringify({
                
            })
        })
        .then(response => response.json())
        .then (data => this.setState({ scraped: data.count }))
    }

    handleEndSearch(){

        const fetchUrl = '/api/endScrapeAPI/';

        fetch(fetchUrl, {
            method: 'POST',
            body: JSON.stringify({
                endScrapeAPI: true
            })
        })
        .then((response) => response.json())
        .then (data => this.setState({ scraped: data.count }))
        
    }
    handleNewSearch(){

    }

    render() {
        return (
            <div className="searchingContentContainer">
                <div className="searchingTitleContainer">
                    <label className="searchingTitle">
                        Searching
                    </label>
                </div>
                <div className="searchingContent">
                    <SettingsButton className="settingsButton"></SettingsButton>
                    <div className="searchingDataContent">
                        <SearchingDataContent title="User:" data={this.props.user}></SearchingDataContent>
                        <SearchingDataContent title="HashTag(s):" data={this.props.hashTags}></SearchingDataContent>
                        <SearchingDataContent title="Location(s):" data={this.props.locations}></SearchingDataContent>
                        <SearchingDataContent title="Phrase(s):" data={this.props.phrases}></SearchingDataContent>
                    </div>
                    <div className="searchingScrapeDataContent">
                        <text>{this.state.scraped} {this.props.platform} Found</text>
                    </div>
                </div>
                <div className="searchingButtonsContainer">
                    <Link to='/HomePage'>
                        <button className="searchingEndButton" onClick={this.handleEndSearch}>
                            End Search
                        </button>
                    </Link>
                    <Link to='/SearchCriteriaPage'>
                        <button className="searchingNewButton" onClick={this.handleNewSearch}>
                            New Search
                        </button>
                    </Link>
                </div>
            </div>
        )
    }
}
