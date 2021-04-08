"""
Created by: Griffin Fluet and Ryan Handlon
Created on: Feb 2021
Version: 1.0
Description: This file contains two functions for scraping Twitter. One for 
building queries to pass into the api call. Another for making the call to the 
api and scraping the data and getting to ready for archiving.
"""
import csv, os, re, requests, threading, tweepy, xlsxwriter
from TwitterConfig import s_consumer_key, s_consumer_secret_key, s_access_token, s_access_token_secret
from datetime import datetime

def v_scrape_tweets(s_query, i_count=50, s_earliest=None, s_latest=None):
    """ 
    Tweet scraper function, collects tweets from Twitter's API and scrapes 
    the text as well as the media of a tweet if it exists. Function results in a 
    zip archive containing a CSV file with scraped text along with a directory for 
    the media that was scraped. 

    Arguments:
    - s_query - string - filter/rules of tweets to find. More on query structure here: 
    https://developer.twitter.com/en/docs/labs/recent-search/guides/search-queries
    - i_count - integer - number of tweets to collect
    - s_earliest - string - earliest date in yyyyMMddHHmm format to search from, this is None by default
    - s_latest - string - latest date in yyyyMMddHHmm format to search to, this is None by default

    Output: Function does not return a value.
    """
    
    # Making connection to API
    o_auth = tweepy.OAuthHandler(s_consumer_key,s_consumer_secret_key)
    o_auth.set_access_token(s_access_token,s_access_token_secret)
    # Creating api object to call tweepy functions
    o_api = tweepy.API(o_auth)
    # Setup of directories for scraped data
    s_now = datetime.now().strftime("%d-%m-%Y_%H")
    s_main_directory = f'./{s_now}/'
    s_media_directory = f'{s_main_directory}media/'
    os.makedirs(s_media_directory,exist_ok=True)
    # Creating the CSV file to be written to
    f_csv = open(f'{s_main_directory}scrape.csv', 'w', encoding = "utf-8")
    # Setting fields for csv formatting
    l_fields = [
        'Post ID',
        'Date',
        'Time',
        'Username',
        'Screen Name',
        'Tweet',
        'Reply Count',
        'Retweet Count',
        'Likes',
        'Location',
        'Link']
    # Object to write to csv file
    o_writer = csv.DictWriter(f_csv,dialect='excel',fieldnames=l_fields)
    o_writer.writeheader()

    # Call to api made here, this returns a list of tweet objects
    # Checkout the attributes of a tweet object here: 
    # https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
    # Need to pass in the developer environment here to gain access to full archive
    # You can find more about the developer environment on the developer portal:
    # https://developer.twitter.com/en
    l_tweets = o_api.search(q=s_query,count=i_count)
    #l_tweets = o_api.search_full_archive('dev',query=s_query,maxResults=i_count,fromDate=s_earliest,toDate=s_latest)
    
    # Using i as the iterative loop value and tweet id
    for i in range(len(l_tweets)):
        # Add 1 so counting is human like 
        i_tweet_id = i + 1
        s_created_at = l_tweets[i].created_at
        s_username = l_tweets[i].user.name
        s_screen_name = l_tweets[i].user.screen_name
        s_text = l_tweets[i].text
        i_reply_count = 'NA'
        #i_reply_count = l_tweets[i].reply_count
        i_retweet_count = 'NA'
        #i_retweet_count = l_tweets[i].retweet_count
        i_likes = l_tweets[i].favorite_count
        s_location = l_tweets[i].place
        s_url = 'https://twitter.com/i/web/status/' + l_tweets[i].id_str

        # Need to parse out date and time from created_at attribute
        o_split_date = re.search(r'(\d\d\-\d\d\-\d\d) (\d\d\:\d\d\:\d\d)',str(s_created_at))
        s_date = o_split_date.group(1)
        s_time = o_split_date.group(2)

        # Writing scraped data points to csv file
        o_writer.writerow({
            'Post ID' : i_tweet_id,
            'Date' : s_date,
            'Time' : s_time,
            'Username' : s_username,
            'Screen Name' : s_screen_name,
            'Tweet' : s_text,
            'Reply Count' : i_reply_count,
            'Retweet Count' : i_retweet_count,
            'Likes' : i_likes,
            'Location' : s_location,
            'Link' : s_url
        })

        # Checking for media in the extended_entities attribute of tweet object
        # More info about the extended_entities attribute can be found here:
        # https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/extended-entities
        if hasattr(l_tweets[i], "extended_entities"):
            i_media_count = 1       # Integer, used to index media names should the tweet object have more than one
            # For each piece of media in extended entities
            for o_media in l_tweets[i].extended_entities["media"]:
                # Find media type, build file name with associated type and ID, and save link to media in s_media_link
                if (o_media['type'] == "photo"):
                    s_media_name = f"{s_media_directory}photoID#{str(i_tweet_id).zfill(5)}-{str(i_media_count)}.jpg"
                    s_media_link = o_media['media_url_https']
                elif (o_media['type'] == "video"):
                    s_media_name = f"{s_media_directory}videoID#{str(i_tweet_id).zfill(5)}-{str(i_media_count)}.mp4"
                    s_media_link = o_media['video_info']['variants'][0]['url']
                elif (o_media['type'] == "animated_gif"):
                    # Gif's are saved as .mp4's because that's how twitter stores them, as shown in the extended_entities object link above
                    s_media_name = f"{s_media_directory}gifID#{str(i_tweet_id).zfill(5)}-{str(i_media_count)}.jpg"
                    s_media_link = o_media['video_info']['variants'][0]['url']

                # Request s_media_link and download it's contents to s_media_name
                o_request = requests.get(s_media_link)
                with open(s_media_name, 'wb') as f_media:
                    f_media.write(o_request.content)

                i_media_count += 1

    # Zipping directory
    os.system(f'zip -r -qq -9 twitter_scrape_from_{s_now}.zip {s_now}')
    # Removing the directory
    os.system(f'rm -rf {s_now}') 

def s_build_query (l_hashtags=None, l_locations=None, l_phrases=None):
    """ 
    Query builder function, builds a query specifying the 
    types of tweets wished to be returned when query is passed to 
    a tweet search using the Twitter API. Function results in a 
    string being returned that is the built query.
    Info on query string being built can be found here:
    https://developer.twitter.com/en/docs/labs/recent-search/guides/search-queries

    No more than 10 total hashtags, locations, and phrases should be inputted.

    Arguments:
    - l_hashtags  - list   - a list of strings, the strings representing hashtags to be searched by
                           - strings should be in the format of "#hashtag" or "hashtag" 
                           - This is None by defalt
    - l_locations - list   - a list of strings, the strings representing locations to be searched by
                           - strings should be in the format of "New York" or ""New York"" 
                           - This is None by defalt
    - l_phrases   - list   - a list of strings, the strings representing phrases to be searched by
                           - strings should be in the format of "I hate Mondays!" or ""I hate Mondays!"" 
                           - This is None by defalt

    Output: 
    - s_query     - string - the query to be used to search tweets
                           - final query will look like "(#hashtag OR #hashtag) ("location" OR "location") ("phrase" OR "phrase")"
                    
    """

    s_query = ""      # String, holds query as it's being built

    # If there are hashtags to be added to query
    if (l_hashtags != None and l_hashtags != [""] and l_hashtags != []):
        s_query = s_query + "("
        # Iterate through each hashtag 
        for s_tag in l_hashtags:
            # Store original hashtag in case it needs do be formatted
            s_old_tag = s_tag
            # Add "#" in front of hashtag if not already there
            if (s_tag.find("#") != 0):
                s_tag = "#" + s_tag
            # If last hashtag add hashtag + ")", else add hashtag + " OR"
            if (l_hashtags.index(s_old_tag) == len(l_hashtags) - 1):
                s_query = s_query + s_tag + ") "
            else:
                s_query = s_query + s_tag + " OR "

    # If there are locations to be added to query
    if (l_locations != None and l_locations != [""] and l_locations != []):
        s_query = s_query + "("
        # iterate through each location 
        for s_loc in l_locations:
            s_old_loc = s_loc
            # Surround locations in quotes if not already there
            if not(s_loc.startswith("\"") and s_loc.endswith("\"")):
                s_loc = "\"" + s_loc + "\""
            # If last hashtag add hashtag + ")", else add hashtag + " OR"
            if (l_locations.index(s_old_loc) == len(l_locations) - 1):
                s_query = s_query + "place:" + s_loc + ") "
            else:
                s_query = s_query + "place:" + s_loc + " OR " 

    # If there are phrases to be added to query
    if (l_phrases != None and l_phrases != [""] and l_phrases != []):
        s_query = s_query + "("
        # Iterate through each phrase 
        for s_phrase in l_phrases:
            s_old_phrase = s_phrase
            # Surround phrase in quotes if not already there
            if not(s_phrase.startswith("\"") and s_phrase.endswith("\"")):
                s_phrase = "\"" + s_phrase + "\""
            # If last phrase add phrase + ")", else add phrase + " OR"
            if (l_phrases.index(s_old_phrase) == len(l_phrases) - 1):
                s_query = s_query + s_phrase + ") "
            else:
                s_query = s_query + s_phrase + " OR " 
    
    # Return query
    return s_query

# v_scrape_tweets('dog')
