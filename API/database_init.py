from api import o_db, UserDB

# Make the database
o_db.create_all()

# Make a user
initialEntry = UserDB(s_email = "socialscraper24@gmail.com", s_password = "asdvaksdbv3@2krnfeGVLM", s_first = "admin", s_last = "account", b_admin = True, b_approved = True, b_banned = False, s_saveEntry1 = "", s_saveEntry2 = "", s_saveEntry3 = "", s_saveEntry4 = "", s_saveEntry5 = "")

# Save and persist that user to the database.
o_db.session.add(initialEntry)
o_db.session.commit()