"""
Created by: Abdul Karim
Created on: Feb 2021
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
   # todo: PendingAccount colum = True/False
   # todo: Need to add last x searches for search histroy functionality

   def __str__(self):
      return f'{self.id} {self.content}'

@m_app.route('/api/loginUser/', methods = ['POST'])
def json_loginUser():
   """
   Description: Allows a frontend process to validate if user credentials are correct.
   Arguements: Non, but json body requested needs to look like this:
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

# User creation is happening. Check to see if the email is already in use and if not,
# Create a new user entry.
@m_app.route('/api/createUser/', methods = ['POST'])
def createUser():   
   """
   Description: Allows a frontend process to create a user and store that user in the database.
   Arguements: Non, but json body requested needs to look like this:
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

               # Check the user database before creating the user.
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

#DONE
@m_app.route('/api/deleteUser/', methods=['POST'])
def delete():
   # Get the user information. JSON Body: {"email": "email@email.com"}
   json_request_data = json.loads(request.data)
   s_inputEmail = json_request_data['email'] 
   
   # Check to see if the user exists
   # exists = o_db.session.query(UserDB.email).filter_by(email=inputEmail).first()
   if(o_db.session.query(UserDB.s_email).filter_by(s_email = s_inputEmail).delete()):
      o_db.session.commit()
      return jsonify({'result': 'OK User deleted'})
   else:
      return jsonify({'result': 'NOK User does not exist'})

# This needs to go
# # Edit a user DO AFTER PRESENTATION DEADLINE
# @m_app.route('/api/editUser/', methods=['POST'])
# def edit():
#    pass

################################################################################
#
#
# INSTAGRAM SCRAPING ENDPOINTS
#
#
################################################################################
# DONE
@m_app.route('/api/scrapeInstagram/', methods =['POST'])
def scrapeInstagram():
   # Get the user information. JSON body: {"search_term": "hashtag/person/location", "search_category": "hashtag or location"}
   json_request_data = json.loads(request.data)

   s_search_term = json_request_data['search_term']
   s_search_category = json_request_data['search_category']

   v_url_extractor(s_search = s_search_term, s_category = s_search_category)
   v_read_to_queue()
   return jsonify({'result': 'Instagram Query Complete'})

################################################################################
#
#
# TWITTER SCRAPING ENDPOINTS
#
#
################################################################################

# Make sure this isn't set to have GET with it as well.
# Done
@m_app.route('/api/scrapeTwitter/', methods=['POST'])
def scrapeTwitter():
   # Get the user information. All lists are comma-serparated. JSON body: {"#hashTags": "#list#of#tags", "locations": "#list#of#locations", "phrases": "#list#of#phrases", "earliestDate": "yyyyMMddHHmm", "latestDate": "yyyyMMddHHmm"}
   json_request_data = json.loads(request.data)

   # Fix this so that we don't have .split(",")
   l_hashTags = json_request_data['hashTags'].split("#")
   l_hashTags.pop(0)
   l_locations = json_request_data['locations'].split("#")
   l_locations.pop(0)
   l_phrases = json_request_data['phrases'].split("#")
   l_phrases.pop(0)
   b_earliest_date = None
   b_latest_date = None  

   if(json_request_data['earliestDate'] != "" and json_request_data['latestDate'] != ""):
      b_earliest_date = json_request_data['earliestDate']
      b_latest_date = json_request_data['latestDate']

   # Set empty lists ([]) to None
   if (len(l_hashTags) <= 0):
      l_hashTags = None
   elif (len(l_locations) <= 0):
      l_locations = None
   elif (len(l_phrases) <= 0):
      l_phrases = None

   s_query = s_build_query(l_hashTags, l_locations, l_phrases)
   v_scrape_tweets(s_query = s_query, s_earliest = b_earliest_date, s_latest = b_latest_date)

   return jsonify({'result': 'Twitter Query Complete'})

# todo: Must return what date range the uses can select from so the calendar can be generated with that information.
# todo: m_app.route to send email
# @m_app.route('/api/getTwitterDateRange', methods=['GET'])
# def getEarlyLateRange():
#    pass

################################################################################
#
#
# SCAFFOLDING
#
#
################################################################################
if __name__ == '__main__':
   m_app.run(debug = True)

# Initialize the DB Model with a user example.
# python3
# from api import o_db
# o_db.create_all ()

# from api import UserDB
# user = UserDB(email = "a2a.a", password = "foo", first = "bar", last = "pie", admin = True, approved = True)
# o_db.session.add(user)
# o_db.session.commit()

# ------------------------------------------------------------------------------

# create TABLE users (
#     id INTEGER not null,
#     can_view_records BOOLEAN not null,
#     PRIMARY KEY (id)
# );

# #someone goes to /api/ any id, pass back that id
# @m_app.route('/api/<int:id>')
# def show(id):
#    print ("This is the id: " + str(id))
#    return jsonify([*map(user_serializer, UserDB.query.filter_by(id=id))])

