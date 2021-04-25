from ScrapeHelper import ScrapeHelper
import tweepy

s_user = "Griffin@mail.com"
s_platform = "twitter"

o_scrape_helper = ScrapeHelper(s_user, s_platform)

def test_api_connection():
    if o_scrape_helper.o_api.verify_credentials():
        return True
    else:
        return False 

assert test_api_connection() == True, "Connection failed"
print('Test Passed')