"""
Created by: Abdul Karim
Created on: 03/31/21
Version: 1.0
Description: File contains the database schema for the user database as well as endpoints that can be used to access backend processes and the database.
"""
from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
import sys

sys.path.insert(1, './twitter')
from TweetExtractor import v_scrape_tweets, s_build_query

sys.path.insert(1, './instagram')
from InstagramKeywordURLExtractor import v_url_extractor
from PostExtractor import v_read_to_queue

# Flask application initiation.
m_app = Flask(__name__)
m_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///userInfo.db"
o_db = SQLAlchemy(m_app)

"""
Name: Abdul Karim
Date Created: 03/31/21
Version: 1.0
Description: The database schema we'll be using to create our user table.
"""
class UserDB(o_db.Model):
   # All of these show the columns of the table in our database.
   s_email = o_db.Column(o_db.Text, nullable = False, primary_key = True)
   s_password = o_db.Column(o_db.Text, nullable = False)
   s_first = o_db.Column(o_db.Text, nullable = False)
   s_last = o_db.Column(o_db.Text, nullable = False)
   b_admin = o_db.Column(o_db.Boolean, nullable = False)
   b_approved = o_db.Column(o_db.Boolean, nullable = False)
   b_logged = o_db.Column(o_db.Boolean, nullable = False)

   
   def __str__(self):
      return f'{self.id} {self.content}'

@m_app.route('/api/authenticateLogin/', methods = ['GET','POST'])
def _json_login_user():
   """
   Description: Allows a frontend process to validate if user credentials are correct.
   Arguements: None, but json body requested needs to look like this:
               {
                  "email": "email@email.com",
                  "password": "password"
               }
   Outputs: JSON body signaling whether or not the information has been validated.    
            Looks like this:
            {
               "result": "OK/NOK followed by a message."
            }
   """
   # Grabbing input information
   json_request_data = json.loads(request.data)
   s_inputEmail = json_request_data['email']
   s_inputPassword = json_request_data['password']

   # Check if the information is within the database
   o_user = o_db.session.query(UserDB).filter_by(s_email = s_inputEmail).first()
   if(o_user != None):
      # Check to see if the password is the empty
      if(s_inputPassword != ""):
         # Check to see if the password matches the one in the DB
         if(s_inputPassword == o_user.password):
            return jsonify({'result': 'OK Email/Password Validated'})
         else:
            return jsonify({'result': 'NOK Email/Password Invalid'})
      else:
         return jsonify({'result': 'NOK Password Field Blank'})
   else:
      return jsonify({'result': 'NOK User Not Found'})

@m_app.route('/api/createUser/', methods = ['GET','POST'])
def _json_create_user():   
   """
   Description: Allows a frontend process to create a user and store that user in the database.
   Arguements: None, but json body requested needs to look like this:
               {
                  "email": "email@email.com",
                  "name": "First Last",
                  "password": "password",
                  "admin": True,
                  "approved": False
               }
   Outputs: JSON body signaling whether or not the information has been validated.    
            Looks like this:
            {
               "result": "OK/NOK followed by a message."
            }
   """
   # Grab all inputs
   json_request_data = json.loads(request.data)

   s_input_email = json_request_data['email']
   s_input_password = json_request_data['password']
   s_input_first_name = ""
   s_input_last_name = ""
   b_input_admin = json_request_data['admin']
   b_input_approved = json_request_data['approved']

   # Special logic to split the name that is passed in.
   l_split_names = json_request_data['name'].split(" ")
   if(len(l_split_names) > 2):
      return jsonify({'result': "NOK Too Many Names Passed In"})
   elif(len(l_split_names) < 2):
      return jsonify({'result': "NOK Too Few Names Passed In"})
   else:
      s_input_first_name = l_split_names[0]
      s_input_last_name = l_split_names[1]

   #This needs to be better handled to return a list of what input fields are empty.
   if(s_input_email != ""):
      if(s_input_password != ""):
         if(s_input_first_name != ""):
            if(s_input_last_name != ""):
               # Build out a user to put into the DB
               o_user = UserDB(s_email = s_input_email, s_first = s_input_first_name, s_last = s_input_last_name, s_password = s_input_password, b_admin = b_input_admin, b_approved = b_input_approved)

               # Check if the user is in the database before creating the user.
               o_exists = o_db.session.query(UserDB.email).filter_by(s_email = user.email).first()
               if(o_exists is None):
                  # Store the user in the User DB
                  o_db.session.add(o_user)
                  o_db.session.commit()
                  return jsonify({'result': 'OK User Created'})  
               else:
                  return jsonify({'result': 'NOK User is already in Database'})
            else:
               return jsonify({'result': 'NOK No Last Name Found'})
         else:
            return jsonify({'result': 'NOK No First Name Found'})
      else:
         return jsonify({'result': 'NOK No Password Found'})
   else:
      return jsonify({'result': 'NOK No Email Input'})

@m_app.route('/api/deleteUser/', methods=['GET','POST'])
def _json_delete_user():
   """
   Description: Allows a frontend process to access the database and delete a user.
   Arguements: None, but json body requested needs to look like this:
               {
                  "email": "email@email.com",
               }
   Outputs: JSON body signaling whether or not the information has been validated.    
            Looks like this:
            {
               "result": "OK/NOK followed by a message."
            }
   """
   # Grab inputs
   json_request_data = json.loads(request.data)
   s_inputEmail = json_request_data['email'] 
   
   # Check to see if the user exists
   if(o_db.session.query(UserDB.s_email).filter_by(s_email = s_inputEmail).delete()):
      o_db.session.commit()
      return jsonify({'result': 'OK User deleted'})
   else:
      return jsonify({'result': 'NOK User does not exist'})

@m_app.route('/api/scrapeInstagram/', methods =['GET','POST'])
def _json_scrape_instagram():
   """
   Description: Allows a frontend process to process a request to scrape instagram, given inputs.
   Arguements: None, but json body requested needs to look like this:
               {
                  "search_term": "#hashtag#stuff OR locationurl",
                  "search_category": "the word: hashtag or the word: location"
                  "email": "a@a.a"
               }
   Outputs: JSON body signaling whether or not the information has been validated.    
            Looks like this:
            {
               "result": "OK/NOK followed by a message."
            }
   """
   # Grab inputs
   json_request_data = json.loads(request.data)

   s_search_term = json_request_data['search_term']
   s_search_category = json_request_data['search_category']

   # Call the function that scrapes instagram.
   v_url_extractor(s_search = s_search_term, s_category = s_search_category)
   v_read_to_queue()

   # have a try catch that returns true or false based on if we can scrape or not. Based on the S_OK value,
   # we do read_to_queue and we also return jsonify OK or NOK

   # an email, the criteria. Then we'd put it into the database.
   # make a foreign key per user that links to that database.

   return jsonify({'result': 'OK Instagram Query Complete'})

@m_app.route('/api/scrapeTwitter/', methods=['GET','POST'])
def _json_scrape_twitter():
   """
   Description: Allows a frontend process to process a request to scrape instagram, given inputs.
   Arguements: None, but json body requested needs to look like this:
               {
                  "#hashTags": "#list#of#tags",
                  "locations": "#list#of#locations",
                  "phrases": "#list#of#phrases",
                  "earliestDate": "yyyyMMddHHmm",
                  "latestDate": "yyyyMMddHHmm"
               }
   Outputs: JSON body signaling whether or not the information has been validated.    
            Looks like this:
            {
               "result": "OK/NOK followed by a message."
            }
   """
   # Grab inputs
   json_request_data = json.loads(request.data)

   l_hashTags = json_request_data['hashTags'].split("#")
   l_hashTags.pop(0)
   l_locations = json_request_data['locations'].split("#")
   l_locations.pop(0)
   l_phrases = json_request_data['phrases'].split("#")
   l_phrases.pop(0)
   s_earliest_date = None
   s_latest_date = None  

   if(json_request_data['earliestDate'] != "" and json_request_data['latestDate'] != ""):
      s_earliest_date = json_request_data['earliestDate']
      s_latest_date = json_request_data['latestDate']

   # Set empty lists ([]) to None
   if (len(l_hashTags) <= 0):
      l_hashTags = None
   elif (len(l_locations) <= 0):
      l_locations = None
   elif (len(l_phrases) <= 0):
      l_phrases = None

   # Run a twitter scrape
   s_query = s_build_query(l_hashTags, l_locations, l_phrases)
   v_scrape_tweets(s_query = s_query, s_earliest = s_earliest_date, s_latest = s_latest_date)

   return jsonify({'result': 'OK Twitter Query Complete'})

def _json_user_serializer(user):
   """
   Description: Prints out all of the files from the database.
   Arguements: User - The user we're trying to scrape from the database.
   Outputs: N/A
   """
   return {
      'email': user.s_email,
      'password': user.s_password,
      'first_name': user.s_first,
      'last_name': user.s_last,
      'admin': user.b_admin,
      'account_approved': user.b_approved
   }

@m_app.route('/api', methods=['GET'])
def _json_userTable():
   """
   Description: Shows us everything in the database. Upgrade to admin-only functionaklity later.
   Arguements: N/A
   Outputs: N/A
   """
   _dict_user_records = UserDB.query.all()
   return jsonify([*map(_json_user_serializer, UserDB.query.all())])

# /contact: ContactUsPage - Input an Email and Message (no longer than 140 characters) and outputs an email to the administrator account that contains the message body. 
@m_app.route('/contact', methods=['GET', 'POST'])
def _json_contact_form_submit():
   """
   Description: Allows the frontend process to send an email to the admin account with a contact request.
   Arguements: None, but json body requested needs to look like this:
               {
                  "s_user_email": "a@a.a",
                  "s_message": "Foo Bar Pie needs account approval?"
               }
   Outputs: JSON body signaling if the message was sent or not.  
            Looks like this:
            {
               "result": "OK/NOK based on if the message was sent to the specified admin account."
            }
   """
   #todo
   _dict_user_records = UserDB.query.all()
   return jsonify([*map(_json_user_serializer, UserDB.query.all())])

# /recentSearches: HomePage - Queries the DB for 5 columns each containing a record of the most recent searches. 
@m_app.route('/recentSearches', methods=['GET', 'POST'])
def _json_get_recent_searches():
   """
   Description: Queries the database's columns for a specific user and returns the 5 most recent searches.
                This information is stored in the database with the following format: platform,mm/dd/yyyy,#keyword#string,-location-string,~phrase~string
   Arguements: None, but json body requested needs to look like this:
               {
                  "s_user_email": "a@a.a",
               }
   Outputs: A deserialized version of the 5 most recent scrapes from the database. If a piece of information
            relating to a scrape doesn't exist, that return value will be empty.
            The output looks like this (note: this returns an empty list if there is no recent search,
            and an abbreviated list if there are less than 5 searches):
            [
               {
                  "s_platform": "One of these two: Instagram OR Twitter",
                  "s_date_scraped": "mm/dd/yyyy",
                  "s_hashtags": "#keyword#string",
                  "s_location": "-location-string",
                  "s_phrases": "~phrase~string"
               },
               ...
            ]
   """
   _dict_user_records = UserDB.query.all()
   return jsonify([*map(_json_user_serializer, UserDB.query.all())])

# /saveSearch: HomePage - moves every other recent search down one column in our database and adds it to the front of the DB. Tracks the date and time associated with the search along with the platform and search keywords. Store as a serialized value, comma-separated. If any commas exist in the input, replace those with a \
@m_app.route('/saveSearch', methods=['GET', 'POST'])
def _json_contact_save_search():
   """
   Description: Takes the most recent search passed in and serializes it for storage. We can then move every other
                search down a column in the user's database and chop off the oldest search query. This information 
                is stored in the database with the following format: platform,mm/dd/yyyy,#keyword#string,
                -location-string,~phrase~string. We also create the time constant
                since it's easily done in the backend.

   Arguements: None, but json body requested needs to look like this:
               {
                  "s_user_email": "a@a.a",
                  "s_platform": "One of these two: Instagram OR Twitter",
                  "s_hashtags": "#keyword#string",
                  "s_location": "-location-string",
                  "s_phrases": "~phrase~string"
               }
   Outputs: Puts a serialized version of the information into the userDB. Returns OK if user was found
            and operation was a success. Else, returns NOK. Looks like this:
            {
               "result": "OK/NOK based on if the serialization was a success or not."
            }
   """
   pass

# /allAccounts: settingsPage - Returns all information from the userDB concerning 
@m_app.route('/getAllAccounts', methods=['GET'])
def _json_get_all_accounts():
   """
   Description: Takes all of the information per user and outputs it so that the front end system can
                display them in the settings page as a list with options to approve/ban/admin/delete accounts.
   Arguements: None
   Outputs: A list of all users. User Account information is stored in each object (note: if there are no users,
            an empty collection will be returned). Looks like this:
            [
               {
                  "s_email" = "a@a.a"
                  "s_first" = "Jane"
                  "s_last" = "Doe"
                  "b_admin" = True OR False
                  "b_approved" = True OR False
                  "b_logged" = True OR False
               },
               ...
            ]
   """
   pass

# /toggleBan: adminSettingsPage - Takes in an email and a boolean value. Sets the value of the banned column for that user, returning an OK for success and NOK if the email doesn't exist.
@m_app.route('/toggleBan', methods=['GET', 'POST'])
def _json_toggle_ban():
   """
   Description: Takes in an email and a boolean value. Sets the value of the banned column for that user, returning 
                an OK for success and NOK if the email doesn't exist.
   Arguements: None, but json body requested needs to look like this:
               {
                  "s_user_email": "a@a.a",
                  "b_ban_value": "True OR False"
               }
   Outputs: An OK result message of the user was found and the value is changed and matches the input value.
            An NOK if the email is not found and the value is not changed.
            [
               {
                  "result": "OK/NOK based on if the user is found or not."
               },
               ...
            ]
   """
   pass

# /toggleApproval: adminSettingsPage - Takes in an email and a boolean value. Sets the value of the approved column for that user, returning an OK for success and NOK if the email doesn't exist.
@m_app.route('/toggleApproval', methods=['GET', 'POST'])
def _json_toggle_approved():
   """
   Description: Takes in an email and a boolean value. Sets the value of the approved column for that user, 
                returning an OK for success and NOK if the email doesn't exist.
   Arguements: None, but json body requested needs to look like this:
               {
                  "s_user_email": "a@a.a",
                  "b_approval_value": "True OR False"
               }
   Outputs: An OK result message of the user was found and the value is changed and matches the input value.
            An NOK if the email is not found and the value is not changed.
            [
               {
                  "result": "OK/NOK based on if the user is found or not."
               },
               ...
            ]
   """
   pass

# /toggleAdmin: adminSettingsPage - Takes in an email and a boolean value. Sets the value of the admin column for that user, returning an OK for success and NOK if the email doesn't exist.
@m_app.route('/toggleAdmin', methods=['GET', 'POST'])
def _json_toggle_approved():
   """
   Description: Takes in an email and a boolean value. Sets the value of the admin column for that user, 
                returning an OK for success and NOK if the email doesn't exist.
   Arguements: None, but json body requested needs to look like this:
               {
                  "s_user_email": "a@a.a",
                  "b_admin_value": "True OR False"
               }
   Outputs: An OK result message of the user was found and the value is changed and matches the input value.
            An NOK if the email is not found and the value is not changed.
            [
               {
                  "result": "OK/NOK based on if the user is found or not."
               },
               ...
            ]
   """
   pass

# /toggleLogged: settingsPage - Takes in an email and a boolean value. Sets the value of the loggedIn column for that user, returning an OK for success and NOK if the email doesn't exist.
@m_app.route('/toggleLogged', methods=['GET', 'POST'])
def _json_toggle_logged():
   """
   Description: Takes in an email and a boolean value. Sets the value of the logged column for that user, 
                returning an OK for success and NOK if the email doesn't exist.
   Arguements: None, but json body requested needs to look like this:
               {
                  "s_user_email": "a@a.a",
                  "b_log_value": "True OR False"
               }
   Outputs: An OK result message of the user was found and the value is changed and matches the input value.
            An NOK if the email is not found and the value is not changed.
            [
               {
                  "result": "OK/NOK based on if the user is found or not."
               },
               ...
            ]
   """
   pass

# Starts the application when this function is started.
if __name__ == '__main__':
   m_app.run(debug = True, host = '0.0.0.0')