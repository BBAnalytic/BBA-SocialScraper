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

################################################################################
#
#
# DATABASE LOGIC
#
#
################################################################################
# Creat a model
class UserDB(o_db.Model):
   email = o_db.Column(o_db.Text, nullable = False, primary_key = True)
   password = o_db.Column(o_db.Text, nullable = False)
   first = o_db.Column(o_db.Text, nullable = False)
   last = o_db.Column(o_db.Text, nullable = False)
   admin = o_db.Column(o_db.Boolean, nullable = False)
   approved = o_db.Column(o_db.Boolean, nullable = False)
   # todo: PendingAccount colum = True/False
   # todo: Need to add last x searches for search histroy functionality

   def __str__(self):
      return f'{self.id} {self.content}'

# DONE
def user_serializer(user):
   return {
      'email': user.email,
      'password': user.password,
      'first_name': user.first,
      'last_name': user.last,
      'admin': user.admin,
      'account_approved': user.approved
   }

################################################################################
#
#
# DATABASE ENDPOINTS
#
#
################################################################################
# DONE
# Shows us everything in the database. Upgrade to admin-only functionaklity later.
@m_app.route('/api', methods=['GET'])
def index():
   users = UserDB.query.all()
   return jsonify([*map(user_serializer, UserDB.query.all())])

# INPROGRESS
#User is trying to login. Check to see if the email and password are correct.
@m_app.route('/api/loginUser/', methods = ['GET', 'POST'])
def loginUser():
   # Get the login information. JSON Body: {"email": "email@email.com", "password": "password"}
   # request_data = json.loads(request.data)
   inputEmail = 'a@a.a' #request_data['email']
   inputPassword = 'foo' #request_data['password']

   # Need to add stronger checks here for valid passwordks. DO AFTER PRESENTATION
   # Check if the information is within the database
   # query = o_db.query(UserDB).filter(Users.email==inputEmail, Users.password==inputPassword)
   # return(str(query))
   user = o_db.session.query(UserDB.email).filter_by(email = inputEmail)
   if(user is not None):
      # Check to see if the password is the empty
      password = o_db.session.query(UserDB.email).filter_by(email = inputEmail)
      if(inputPassword is not ""):
         # Check to see if the password matches the one in the DB
         if(password == user.password):
            return jsonify({'result': 'OK Email/Password Validated'})
         else:
            return jsonify({'result': 'NOK Email/Password Invalid'})
      else:
         return jsonify({'result': 'NOK Password Field Blank'})
   else:
      return jsonify({'result': 'NOK User Not Found'})

# DONE
# User creation is happening. Check to see if the email is already in use and if not,
# Create a new user entry.
@m_app.route('/api/createUser/', methods = ['POST'])
def createUser():   
   # Get the user information. JSON Body: {"email": "email@email.com", "name": "First Last", "password": "password", "admin": True, "approved": False}
   request_data = json.loads(request.data)

   # Grab all inputs
   inputEmail = request_data['email']
   inputPassword = request_data['password']
   inputFirstName = ''
   inputLastName = ''
   inputAdmin = request_data['admin']
   inputApproved = request_data['approved']

   # Special logic to split the name that is passed in.
   splitNames = request_data['name'].split(" ")
   if(len(splitNames) > 2):
      return jsonify({'result': "NOK Too Many Names Passed In"})
   elif(len(splitNames) < 2):
      return jsonify({'result': "NOK Too Few Names Passed In"})
   else:
      # splitNames = ['deemo', 'deech']
      inputFirstName = splitNames[0]
      inputLastName = splitNames[1]

   #This needs to be better handled to return a list of what input fields are empty.
   if(inputEmail != ""):
      if(inputPassword != ""):
         if(inputFirstName != ""):
            if(inputLastName != ""):
               # Build out a user to put into the DB
               user = UserDB(email = inputEmail, first = inputFirstName, last = inputLastName, password = inputPassword, admin = inputAdmin, approved = inputApproved)

               # Check the user database before creating the user.
               exists = o_db.session.query(UserDB.email).filter_by(email=user.email).first()
               if(exists is None):
                  # Store the user in the User DB
                  o_db.session.add(user)
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
   request_data = json.loads(request.data)
   inputEmail = request_data['email'] 
   
   # Check to see if the user exists
   # exists = o_db.session.query(UserDB.email).filter_by(email=inputEmail).first()
   if(o_db.session.query(UserDB.email).filter_by(email = inputEmail).delete()):
      o_db.session.commit()
      return jsonify({'result': 'OK User deleted'})
   else:
      return jsonify({'result': 'NOK User does not exist'})

# Edit a user DO AFTER PRESENTATION DEADLINE
@m_app.route('/api/editUser/', methods=['POST'])
def edit():
   pass

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
   request_data = json.loads(request.data)

   search_term = request_data['search_term']
   search_category = request_data['search_category']

   v_url_extractor(s_search = search_term, s_category = search_category)
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
   # Get the user information. All lists are comma-serparated. JSON body: {"#hashTags": "list,of,tags", "locations": "list,of,locations", "phrases": "list,of,phrases", "earliestDate": "yyyyMMddHHmm", "latestDate": "yyyyMMddHHmm"}
   request_data = json.loads(request.data)

   # Fix this so that we don't have .split(",")
   hashTags = request_data['hashTags'].split(",")
   hashTags = hashTags[0].split("#")
   hashTags.pop(0)
   locations = request_data['locations'].split(",")
   locations = locations[0].split("#")
   locations.pop(0)
   phrases = request_data['phrases'].split(",")
   phrases = phrases[0].split("#")
   phrases.pop(0)
   earliestDate = None
   latestDate = None  

   if(request_data['earliestDate'] != "" and request_data['latestDate'] != ""):
      earliestDate = request_data['earliestDate']
      latestdate = request_data['latestDate']

   # Set empty lists ([]) to None
   if (len(hashTags) <= 0):
      hashTags = None
   elif (len(locations) <= 0):
      locations = None
   elif (len(phrases) <= 0):
      phrases = None

   query = s_build_query(hashTags, locations, phrases)
   v_scrape_tweets(s_query = query, s_earliest = earliestDate, s_latest = latestDate)

   return jsonify({'result': 'Twitter Query Complete'})

# todo: Must return what date range the uses can select from so the calendar can be generated with that information.
# todo: m_app.route to send email
@m_app.route('/api/getTwitterDateRange', methods=['GET'])
def getEarlyLateRange():
   pass

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

