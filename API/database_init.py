from api import o_db, UserDB

# Make the database
o_db.create_all()

# Make a user
initialEntry = UserDB(s_email = "socialscraper24@gmail.com", 
                      s_password = "asdvaksdbv3@2krnfeGVLM", 
                      s_first = "admin", 
                      s_last = "account", 
                      b_admin = True, 
                      b_approved = True, 
                      b_banned = False, 
                      s_saveEntry1 = "instagram,05/21/1199,#blm,,,,", 
                      s_saveEntry2 = "twitter,05/21/1199,#minecraft#blm,#new york#york,#asianlivesmatter#pokemonplatinumrelease,05/21/1199,05/21/1199", 
                      s_saveEntry3 = "twitter,05/21/1199,,#new york#york,#asianlivesmatter#pokemonplatinumrelease,05/21/1199,05/21/1199", 
                      s_saveEntry4 = "twitter,05/21/1199,#minecraft#blm,#new york#york,,,", 
                      s_saveEntry5 = "instagram,05/21/1199,,#www.test.com,,,")

# Save and persist that user to the database.
o_db.session.add(initialEntry)
o_db.session.commit()