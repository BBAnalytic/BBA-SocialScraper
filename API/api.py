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
   b_banned = o_db.Column(o_db.Boolean, nullable = False)
   s_col1 = o_db.Column(o_db.Text, nullable = True)
   s_col2 = o_db.Column(o_db.Text, nullable = True)
   s_col3 = o_db.Column(o_db.Text, nullable = True)
   s_col4 = o_db.Column(o_db.Text, nullable = True)
   s_col5 = o_db.Column(o_db.Text, nullable = True)
   
   def __str__(self):
      return f'{self.id} {self.content}'

@m_app.route('/api/authenticateLogin/', methods = ['POST'])
def json_login_user():
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
         # Check to see if the user is approved
         if(o_user.b_approved == True):
            # Check to see if user is banned
            if(o_user.b_banned == False):
               # Check to see if the password matches the one in the DB
               if(s_inputPassword == o_user.password):
                  return jsonify({'result': 'OK Email/Password Validated'})
               else:
                  return jsonify({'result': 'NOK Email/Password Invalid'})
            else:
               return jsonify({'result': 'NOK User us Banned'})
         else:
            return jsonify({'result': 'NOK User is not Approved'})
      else:
         return jsonify({'result': 'NOK Password Field Blank'})
   else:
      return jsonify({'result': 'NOK User Not Found'})

@m_app.route('/api/createUser', methods = ['POST'])
def json_create_user():   
   """
   Description: Allows a frontend process to create a user and store that user in the database. Users
                created initially have their banned, approved, and admin values defaulted to false.
                They also have all saveSearch columns defaulted to empty string ("")
   Arguements: None, but json body requested needs to look like this:
               {
                  "email": "email@email.com",
                  "name": "First Last",
                  "password": "password",
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
               o_user = UserDB(s_email = s_input_email, s_first = s_input_first_name, 
                               s_last = s_input_last_name, s_password = s_input_password, 
                               b_admin = False, b_approved = False, b_banned = False,
                               s_col1 = "", s_col2 = "", s_col3 = "", s_col4 = "",
                               s_col5 = "")

               # Check if the user is in the database before creating the user.
               o_exists = o_db.session.query(UserDB.s_email).filter_by(s_email = o_user.s_email).first()
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

@m_app.route('/api/deleteUser', methods=['POST'])
def json_delete_user():
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
   # json_request_data = json.loads(request.data)
   s_input_email = "b@b.b"#json_request_data['email'] 
   
   # Check to see if the user exists
   if(o_db.session.query(UserDB.s_email).filter_by(s_email = s_input_email).delete()):
      o_db.session.commit()
      return jsonify({'result': 'OK User deleted'})
   else:
      return jsonify({'result': 'NOK User does not exist'})

@m_app.route('/api/scrapeInstagram/', methods =['POST'])
def json_scrape_instagram():
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

@m_app.route('/api/scrapeTwitter/', methods=['POST'])
def json_scrape_twitter():
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

@m_app.route('/getAllAccounts', methods=['GET'])
def json_get_all_accounts():
   """
   Description: Takes all of the information per user and outputs it so that the front end system can
                display them in the settings page as a list with options to approve/ban/admin/delete accounts.
   Arguements: None
   Outputs: A list of all users. User Account information is stored in each object (note: if there are no users,
            an empty collection will be returned). Looks like this:
            [
               {
                  "s_email" : "a@a.a",
                  "s_first" : "Jane",
                  "s_last" : "Doe",
                  "b_admin" : True OR False,
                  "b_approved" : True OR False,
                  "b_banned" : True OR False,
               },
               ...,
               {
                  ...
               }
            ]
   """
   _dict_user_records = UserDB.query.all()
   return jsonify([*map(_json_user_serializer, UserDB.query.all())])

@m_app.route('/getAccount', methods=['POST'])
def json_get_account():
   """
   Description: Takes in an email and processes it to find a user in the database and return its values
   Arguements: None, but json body requested needs to look like this:
               {
                  "s_user_email": "a@a.a",
               }
   Outputs: A object containing the user that is found in the database or NOK if user was not found.
               {
                  "s_email" : "a@a.a",
                  "s_first" : "Jane",
                  "s_last" : "Doe",
                  "b_admin" : True OR False,
                  "b_approved" : True OR False,
                  "b_banned" : True OR False,
               }
            OR
               {
                  "result": "OK/NOK based on if the user is found or not."
               }
   """
   # Grabbing input information
   json_request_data = json.loads(request.data)
   s_input_email = json_request_data['s_user_email']

   # Check if the information is within the database
   o_user = o_db.session.query(UserDB).filter_by(s_email = s_input_email).first()
   if(o_user != None):
      return jsonify({"b_admin": o_user.b_admin, 
                      "b_approved": o_user.b_approved,
                      "b_banned": o_user.b_banned,
                      "s_email": o_user.s_email,
                      "s_first": o_user.s_first,
                      "s_last": o_user.s_first})
   else:
      return jsonify({'result': 'NOK User Not Found'})

def _json_user_serializer(user):
   """
   Description: Prints out all of the files from the database.
   Arguements: User - The user we're trying to scrape from the database.
   Outputs: A JSONified object containing user details.
   """
   return {
      's_email': user.s_email,
      's_first_name': user.s_first,
      's_last_name': user.s_last,
      'b_admin': user.b_admin,
      'b_approved': user.b_approved,
      'b_banned': user.b_banned,
   }

@m_app.route('/toggleBan', methods=['POST'])
def json_toggle_ban():
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
            {
               "result": "OK/NOK based on if the user is found or not."
            }
   """
   # Grabbing input information
   json_request_data = json.loads(request.data)
   s_input_email = json_request_data['s_user_email']
   b_change_value = json_request_data['b_ban_value']

   # Check if the information is within the database
   o_user = o_db.session.query(UserDB).filter_by(s_email = s_input_email).first()
   if(o_user != None):
      # If the value passed in is empty, return an error because we can't set a value that isn't there.
      if(b_change_value != None):
         # Set the value of that user to whatever the input value is.
         if(b_change_value == True):
            o_user.b_banned = True
         elif(b_change_value == False):
            o_user.b_banned = False
         o_db.session.commit()
         return jsonify({'result': 'OK'})
      else:
         return jsonify({'result': 'NOK No change value passed in.'})
   else:
      return jsonify({'result': 'NOK User Not Found'})

@m_app.route('/toggleApprove', methods=['POST'])
def json_toggle_approved():
   """
   Description: Takes in an email and a boolean value. Sets the value of the approved column for that user, 
                returning an OK for success and NOK if the email doesn't exist.
   Arguements: None, but json body requested needs to look like this:
               {
                  "s_user_email": "a@a.a",
                  "b_approve_value": "True OR False"
               }
   Outputs: An OK result message of the user was found and the value is changed and matches the input value.
            An NOK if the email is not found and the value is not changed.
            {
               "result": "OK/NOK based on if the user is found or not."
            }
   """
   # Grabbing input information
   json_request_data = json.loads(request.data)
   s_input_email = json_request_data['s_user_email']
   b_change_value = json_request_data['b_approve_value']

   # Check if the information is within the database
   o_user = o_db.session.query(UserDB).filter_by(s_email = s_input_email).first()
   if(o_user != None):
      # If the value passed in is empty, return an error because we can't set a value that isn't there.
      if(b_change_value != None):
         # Set the value of that user to whatever the input value is.
         if(b_change_value == True):
            o_user.b_approved = True
         elif(b_change_value == False):
            o_user.b_approved = False
         o_db.session.commit()
         return jsonify({'result': 'OK'})
      else:
         return jsonify({'result': 'NOK No change value passed in.'})
   else:
      return jsonify({'result': 'NOK User Not Found'})

@m_app.route('/toggleAdmin', methods=['POST'])
def json_toggle_admin():
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
            {
               "result": "OK/NOK based on if the user is found or not."
            }
   """
   # Grabbing input information
   json_request_data = json.loads(request.data)
   s_input_email = json_request_data['s_user_email']
   b_change_value = json_request_data['b_admin_value']

   # Check if the information is within the database
   o_user = o_db.session.query(UserDB).filter_by(s_email = s_input_email).first()
   if(o_user != None):
      # If the value passed in is empty, return an error because we can't set a value that isn't there.
      if(b_change_value != None):
         # Set the value of that user to whatever the input value is.
         if(b_change_value == True):
            o_user.b_admin = True
         elif(b_change_value == False):
            o_user.b_admin = False
         o_db.session.commit()
         return jsonify({'result': 'OK'})
      else:
         return jsonify({'result': 'NOK No change value passed in.'})
   else:
      return jsonify({'result': 'NOK User Not Found'})

# Starts the application when this function is started.
if __name__ == '__main__':
   m_app.run(debug = True, host = '0.0.0.0')