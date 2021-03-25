import React, { Component } from 'react'
import { Redirect } from 'react-router';

export default class SearchSubmit extends Component {
    constructor(props){
        super(props);
        this.state = {
        };
  
      }

    render() {

        if (this.props.isValidSubmit){
            return (
                <div>
                    <Redirect to='/SearchingPage'></Redirect>
                </div>
            )
        }
        else{
            return (
                <div>
                    <Redirect to='/SearchCriteriaPage'></Redirect>
                </div>
            )
        }
    }
}
