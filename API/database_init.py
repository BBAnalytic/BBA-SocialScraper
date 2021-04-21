from api import o_db
from api import UserDB

# Make the database
o_db.create_all()

# Make a user
initialEntry = UserDB(s_email = "a@a.a", s_password = "bar", s_first = "pie", s_last = "man", b_admin = True, b_approved = True, b_banned = False, s_col1 = "", s_col2 = "", s_col3 = "", s_col4 = "", s_col5 = "")

# Save and persist that user to the database.
o_db.session.add(initialEntry)
o_db.session.commit()

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

   def str(self):
      return f'{self.id} {self.content}'