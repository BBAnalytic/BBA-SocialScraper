import React, { Component } from 'react'
import SettingsButton from './SettingsButton';
import SearchCriteriaInput from './SearchCriteriaInput';
import SearchCriteriaDate from './SearchCriteriaDate';
import './css/SearchCriteriaPage.css'
import HomeButton from './HomeButton';
import { Link, Redirect } from 'react-router-dom';
import NavButtons from './NavButtons'

export default class SearchCriteriaPage extends Component {
    constructor(props){
        super(props);
    }

    render() {
        if (this.props.email != ""){
            return (
                <div className="searchCriteriaPageContainer">
                    <div className="searchPlatformSelectionTitleContainer">
                        <label className="searchPlatformSelectionTitle">
                            Search Platform Selection
                        </label>
                    </div>
                    <div className="searchCriteriaPlatformSelectionContainer">
                        <SettingsButton className="navButtons"></SettingsButton>
                        <div className="platformSearchContentContainer">
                            <div className="platformSelectionContainer">
                                <text className="platformLabel">
                                    Platform:
                                </text>
                                <select className="platformSelector" value={this.props.platformSelector} onChange={ this.props.handleSelection }>
                                    <option value='Select'>Select</option>
                                    <option value='Twitter'>Twitter</option>
                                    <option value='Instagram'>Instagram</option>
                                </select>
                            </div>
                            <div className="searchTypeSelectionContainer">
                                <label className="searchTypeLabel">
                                    Search Type:
                                </label>
                                <select className="searchTypeSelector">
                                    <option value='Basic'>Basic</option>
                                    <option value='Advanced'>Advanced</option>
                                </select>
                            </div>
                        </div>
                        <div className="searchCriteriaFormContentContainer">
                            <div className="searchCriteriaFormLabelContainer">
                                <label className="searchCriteriaFormLabel">
                                    Search Criteria
                                </label>
                            </div>
                            <div className="searchCriteriaFormContainer">
                                <div className="searchByContainer">
                                    <label className="searchByLabel">
                                        Search By:
                                    </label>
                                    <div className="searchByInput">
                                        <div>
                                            <input type="checkbox" id="hashTagCheckBox"></input>
                                            <label for="hashTagCheckBox">HashTags</label>
                                        </div>
                                        <div>
                                            <input type="checkbox" id="locationCheckBox"></input>
                                            <label for="locationCheckBox">Locations</label>
                                        </div>
                                        <div>
                                            <input type="checkbox" id="phraseCheckBox"></input>
                                            <label for="phraseCheckBox">Phrases</label>
                                        </div>
                                    </div>
                                </div>
                                <div className="searchCriteriaContainer">
                                    <SearchCriteriaInput 
                                        searchCriteriaLabel="HashTag(s):" 
                                        searchCriteriaExample="Example: #dog#cat#blackbear" 
                                        searchCriteriaPlaceHolder="#HashTag" 
                                        searchCriteriaValue={this.props.hashTags} 
                                        onSearchCriteriaChange={this.props.handleHashTagsInput}
                                    />
                                    
                                    <SearchCriteriaInput 
                                        searchCriteriaLabel="Location(s):" 
                                        searchCriteriaExample="Example: #newyork#UnitedStates#bangor,ME" 
                                        searchCriteriaPlaceHolder="#Location"
                                        searchCriteriaValue={this.props.locations} 
                                        onSearchCriteriaChange={this.props.handleLocationsInput}
                                    />
                                    {
                                        !this.props.hideComponent &&
                                        <SearchCriteriaInput 
                                            searchCriteriaLabel="Phrase(s):" 
                                            searchCriteriaExample="Example: #working late#I love blackbears" 
                                            searchCriteriaPlaceHolder="#Phrase"
                                            searchCriteriaValue={this.props.phrases} 
                                            onSearchCriteriaChange={this.props.handlePhrasesInput}
                                        />
                                    }
                                </div>
                                {
                                    !this.props.hideComponent &&
                                    <div className="dateSelectionContainer">
                                        <SearchCriteriaDate 
                                            searchCriteriaDateLabel="Start Date:" 
                                            searchCriteriaDateExample="Example: 01/01/2020" 
                                            onSearchCriteriaDateChange={this.props.handleStartDateInput} 
                                        />
                                        <SearchCriteriaDate
                                            searchCriteriaDateLabel="End Date:"
                                            searchCriteriaDateExample="Example: 01/01/2020"
                                            onSearchCriteriaDateChange={this.props.handleEndDateInput}
                                        />
                                    </div>
                                }
                            </div>
                        </div>
                    </div>
                    <Link to='/SearchingPage'>
                        <button className="searchButton" onClick={this.props.handleSearch}>
                            Search
                        </button>
                    </Link>
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
