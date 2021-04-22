import React, { Component } from 'react';
import './App.css'
import LoginPage from './components/LoginPage'
import SearchCriteriaPage from './components/SearchCriteriaPage'
import SearchingPage from './components/SearchingPage';
import HomePage from './components/HomePage'
import SettingsPage from './components/SettingsPage'
import ContactUsPage from './components/ContactUsPage'
import LoginAuthenticate from './components/LoginAuthenticate'
import SearchSubmit from './components/SearchSubmit'
// import RegisterAccountConfirm from './components/RegisterAccountConfirm'
//Test

// Imports from react-router
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  Redirect
} from "react-router-dom";
import AdminSettingsPage from './components/AdminSettingsPage';

export default class App extends Component {
  constructor(props){
      super(props);
      this.state = {
          email: '',
          password: '',
          isAuthenticated: false,
          isValidSubmit: false,
          platformSelector: 'Select',
          hashTags: '',
          locations: '',
          phrases: '',
          startDate: '',
          endDate: ''
      };

      this.handleEmailChange = this.handleEmailChange.bind(this);
      this.handlePasswordChange = this.handlePasswordChange.bind(this);
      this.handleHashTagsInput = this.handleHashTagsInput.bind(this);
      this.handleLocationsInput = this.handleLocationsInput.bind(this);
      this.handlePhrasesInput = this.handlePhrasesInput.bind(this);
      this.handleStartDateInput = this.handleStartDateInput.bind(this);
      this.handleEndDateInput = this.handleEndDateInput.bind(this);
      this.handleSearch = this.handleSearch.bind(this);
      this.handleSelection = this.handleSelection.bind(this);
    }
  
  handleEmailChange(event){
    this.setState({email: event.target.value});
  }

  handlePasswordChange(event){
    this.setState({password: event.target.value});
  }

  handleSelection(newPlatform){
    this.setState({platformSelector: newPlatform.target.value});
    
    if(newPlatform.target.value == "Twitter"){
        this.setState({fetchURL: '/api/scrapeTwitter/'});
    }
    else{
        this.setState({fetchURL: '/api/scrapeInstagram/'});
    }
  }
  handleHashTagsInput(newHashTags){
      this.setState({hashTags: newHashTags});

      if (this.state.platformSelector != 'Select'){
        this.setState({isValidSubmit: true});
      }
  }
  handleLocationsInput(newLocations){
      this.setState({locations: newLocations});
  }
  handlePhrasesInput(newPhrases){
      this.setState({phrases: newPhrases});
  }
  handleStartDateInput(newStartDate){
      this.setState({startDate: newStartDate});
  }
  handleEndDateInput(newEndDate){
      this.setState({endDate: newEndDate});
  }

  handleSearch(event){
  //Handles search POST function
  //If Twitter Platform selected, POST Twitter info
  //Else Instagram Platform selected, POST Instagram info

      if (this.state.platformSelector == 'Twitter'){
          fetch(this.state.fetchURL, {
              method: 'POST',
              body: JSON.stringify({
                  hashTags: this.state.hashTags,
                  locations: this.state.locations,
                  phrases: this.state.phrases,
                  earliestDate: '',
                  latestDate: ''
              })
          })
      }
      else {
          fetch(this.state.fetchURL, {
              method: 'POST',
              body: JSON.stringify({
                  searchTerm: this.state.hashTags,
                  searchCategory: 'hashtag'
              })
          })
      }
  }

  render(){
  return (
    <div className="App">
      <Router>
        <Switch>
          <Route exact path = '/LoginPage'>
            <LoginPage 
              title = 'Log In' 
              email = {this.state.email} 
              password = {this.state.password} 
              handleEmailChange = {this.handleEmailChange} 
              handlePasswordChange = {this.handlePasswordChange} 
              handleLogin = {this.handleLogin} 
            />
          </Route>
          <Route exact path = '/HomePage'>
            <HomePage 
              title = 'HomePage' 
              email = {this.state.email}
            />
          </Route>
          <Route exact path = '/SearchCriteriaPage'>
            <SearchCriteriaPage 
              title = 'Search Criteria'
              platformSelector = {this.state.platformSelector}
              hashTags = {this.state.hashTags}
              locations = {this.state.locations}
              phrases = {this.state.phrases}
              startDate = {this.state.startDate}
              endDate = {this.state.endDate}
              handleSelection = {this.handleSelection}
              handleHashTagsInput = {this.handleHashTagsInput}
              handleLocationsInput = {this.handleLocationsInput}
              handlePhrasesInput = {this.handlePhrasesInput}
              handleStartDateInput = {this.handleStartDateInput}
              handleEndDateInput = {this.handleEndDateInput}
              handleSearch = {this.handleSearch}
            />
          </Route>
          <Route exact path = '/SearchingPage'>
            <SearchingPage 
              title = 'Searching'
              user = 'James West'
              hashTags = { this.state.hashTags }
              locations = 'N/A'
              phrases = 'N/A'
            />
          </Route>
          <Route exact path = '/SettingsPage'>
            <SettingsPage
              title = 'Settings'
              email = {this.state.email}
              />
          </Route>
          <Route exact path = '/AdminSettingsPage'>
            <AdminSettingsPage
              title = 'Admin Settings'
              email = {this.state.email}
             />
          </Route>
          {/* <Route exact path = '/RegisterAccount'>
            <RegisterAccount title = 'Register Account' />
          </Route>
          <Route exact path = '/RegisterAccountConfirm'>
            <RegisterAccountConfirm title = 'Register Account' />
          </Route> */}
          <Route exact path = '/ContactUsPage'>
            <ContactUsPage title='Contact Us'></ContactUsPage>
          </Route>
          <Route exact path = '/LoginAuthenticate'>
            <LoginAuthenticate 
              isAuthenticated={this.state.isAuthenticated}
              email = {this.state.email}
              password = {this.state.email}
            />
          </Route>
          <Route exact path = '/SearchSubmitPage'>
            <SearchSubmit 
              isValidSubmit = { this.state.isValidSubmit }
            />
          </Route>
        </Switch>
      </Router>
    </div>
  );
}
}
