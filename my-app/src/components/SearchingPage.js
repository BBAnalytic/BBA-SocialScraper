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
import { Link, Redirect } from 'react-router-dom';

export default class SearchingPage extends Component {
    constructor(props){
        super(props);
        this.state = {
            scraped: 'Searching and Collecting Data...',  // Number of units that the API has scraped
            user: '',
            hashTags: 'N/A',
            locations: 'N/A',
            phrases: 'N/A'
        }
        
    };

    componentDidMount(){
        const fetchURL = '/api/getAccount';
        const fetchContent = {
            method: 'POST',
            body: JSON.stringify({
                email: this.props.email
            })
        }

        fetch(fetchURL, fetchContent)
            .then(Response => Response.json())
            .then(data => {
                const name = data.s_first + " " + data.s_last;
                
                this.setState({ 
                    user: name
                })
                if (this.props.hashTags !== ""){
                    this.setState({
                        hashTags: this.props.hashTags
                    })
                }
                if (this.props.locations !== ""){
                    this.setState({
                        locations: this.props.locations
                    })
                }
                if (this.props.phrases !== ""){
                    this.setState({
                        phrases: this.props.phrases
                    })
                }
            })
    }

    render() {
        if (this.props.email != ""){
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
                            <SearchingDataContent title="User:" data={this.state.user}></SearchingDataContent>
                            <SearchingDataContent title="HashTag(s):" data={this.props.hashTags}></SearchingDataContent>
                            <SearchingDataContent title="Location(s):" data={this.props.locations}></SearchingDataContent>
                            <SearchingDataContent title="Phrase(s):" data={this.props.phrases}></SearchingDataContent>
                        </div>
                        <div className="searchingScrapeDataContent">
                            <text>{this.state.scraped}</text>
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
        else{
            return(
                <div>
                    <Redirect to='/LoginPage'></Redirect>
                </div>
            )
        }
    }
}
