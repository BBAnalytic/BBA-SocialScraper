import os
from api import o_db, UserDB
# from api import o_db
# from api import UserDB

# Make the database
o_db.create_all()

# Make a user
initialEntry = UserDB(s_email = "a@a.a", s_password = "bar", s_first = "pie", s_last = "man", b_admin = True, b_approved = True, b_banned = False, s_saveEntry1 = "", s_saveEntry2 = "", s_saveEntry3 = "", s_saveEntry4 = "", s_saveEntry5 = "")

# Save and persist that user to the database.
o_db.session.add(initialEntry)
o_db.session.commit()