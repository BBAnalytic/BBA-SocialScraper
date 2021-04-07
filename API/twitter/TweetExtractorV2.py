"""
Created by: Griffin Fluet and Ryan Handlon
Created on: March 2021
Version: 2.0
Description: This file contains two functions for scraping Twitter. One for 
building queries to pass into the api call. Another for making the call to the 
api and scraping the data and getting to ready for archiving.
"""
import csv,os,pickle,re,requests,tweepy
from datetime import datetime as o_datetime
from twitter.TwitterConfig import s_consumer_key, s_consumer_secret_key, s_dev_environment
from twitter.ScrapeHelper import ScrapeHelper

def v_query_seven_day_api(o_scrape_helper):
    """
    This function makes the api call to twitter. Api returns pages of tweets and each 
    page is written to a pickle file for later scraping. Once completed the scraper function is 
    called.

    Arguments:
    - o_scrape_helper - object - instance of the ScrapeHelper object for scrape in progress
    
    Output: This function has no return value.
    """
    i_file_count = 0
    os.makedirs(o_scrape_helper.s_pickle_directory,exist_ok = True)
    for o_page in tweepy.Cursor(o_scrape_helper.o_api.search,q=o_scrape_helper.s_query, tweet_mode = 'extended').pages(3):
        pickle.dump(o_page, open(f'{o_scrape_helper.s_pickle_directory}pickle{i_file_count}.p', 'wb'))
        i_file_count += 1
    v_scrape_seven_day_tweets(i_file_count,o_scrape_helper)

def v_query_full_archive_api(o_scrape_helper):
    """
    This function makes the api call to twitter. Api returns pages of tweets and each 
    page is written to a pickle file for later scraping. Once completed the scraper function is 
    called.

    Arguments:
    - o_scrape_helper - object - instance of the ScrapeHelper object for scrape in progress
    
    Output: This function has no return value.
    """
    i_file_count = 0
    os.makedirs(o_scrape_helper.s_pickle_directory,exist_ok = True)
    for o_page in tweepy.Cursor(o_scrape_helper.o_api.search_full_archive,environment_name=s_dev_environment, query=o_scrape_helper.s_query).pages(3):
        pickle.dump(o_page, open(f'{o_scrape_helper.s_pickle_directory}pickle{i_file_count}.p', 'wb'))
        i_file_count += 1
    v_scrape_full_archive_tweets(i_file_count,o_scrape_helper)

def v_scrape_seven_day_tweets(i_pickles,o_scrape_helper):
    """
    This function is where the data from the tweets will be written to our csv file
    and media from the tweet will be downloaded. Directory creation takes place here and setup
    for writing the csv file.

    Arguments:
    - i_pickles - integer - number of pickles to read through
    - o_scrape_helper - object - instance of the ScrapeHelper object for scrape in progress

    Output: This function has no return value.
    """
    i_id = 1
    # Creation of directories for scraped data
    os.makedirs(o_scrape_helper.s_media_directory,exist_ok=True)
    os.makedirs(o_scrape_helper.s_pickle_directory,exist_ok=True)
    # Creating the CSV file to be written to
    f_csv = open(f'{o_scrape_helper.s_top_directory}scrape.csv', 'w', encoding = "utf-8")
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
    for i in range(i_pickles):
        o_page = pickle.load(open(f'{o_scrape_helper.s_pickle_directory}pickle{i}.p', 'rb'))
        for o_tweet in o_page:
            i_tweet_id = i_id
            i_id += 1
            s_created_at = o_tweet.created_at
            s_username = o_tweet.user.name
            s_screen_name = o_tweet.user.screen_name
            s_text = o_tweet.full_text
            i_reply_count = 'na'
            #i_reply_count = tweet.reply_count
            i_retweet_count = 'na'
            #i_retweet_count = tweet.retweet_count
            i_likes = o_tweet.favorite_count
            s_location = o_tweet.place
            s_url = 'https://twitter.com/i/web/status/' + o_tweet.id_str

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

            # If retweet, set tweet equal to original tweet. This is because the retweeted tweet does not store media, but the original does
            if hasattr(o_tweet, "retweeted_status"):
                o_tweet = o_tweet.retweeted_status

            if hasattr(o_tweet, "extended_entities"):
                i_media_count = 1       # Integer, used to index media names should the tweet object have more than one
                # For each piece of media in extended entities
                for o_media in o_tweet.extended_entities["media"]:
                    # Find media type, build file name with associated type and ID, and save link to media in s_media_link
                    if (o_media['type'] == "photo"):
                        s_media_name = f"{o_scrape_helper.s_media_directory}photoID#{str(i_tweet_id).zfill(5)}-{str(i_media_count)}.jpg"
                        s_media_link = o_media['media_url_https']
                    elif (o_media['type'] == "video"):
                        s_media_name = f"{o_scrape_helper.s_media_directory}videoID#{str(i_tweet_id).zfill(5)}-{str(i_media_count)}.mp4"
                        s_media_link = o_media['video_info']['variants'][0]['url']
                    elif (o_media['type'] == "animated_gif"):
                       # Gif's are saved as .mp4's because that's how twitter stores them, as shown in the extended_entities object link above
                        s_media_name = f"{o_scrape_helper.s_media_directory}gifID#{str(i_tweet_id).zfill(5)}-{str(i_media_count)}.mp4"
                        s_media_link = o_media['video_info']['variants'][0]['url']

                    # Request s_media_link and download it's contents to s_media_name
                    o_request = requests.get(s_media_link)
                    with open(s_media_name, 'wb') as f_media:
                        f_media.write(o_request.content)

                    i_media_count += 1

def v_scrape_full_archive_tweets(i_pickles,o_scrape_helper):
    """
    This function is where the data from the tweets will be written to our csv file
    and media from the tweet will be downloaded. Directory creation takes place here and setup
    for writing the csv file.

    Arguments:
    - i_pickles - integer - number of pickles to read through
    - o_scrape_helper - object - instance of the ScrapeHelper object for scrape in progress

    Output: This function has no return value.
    """
    i_id = 1
    # Creation of directories for scraped data
    os.makedirs(o_scrape_helper.s_media_directory,exist_ok=True)
    os.makedirs(o_scrape_helper.s_pickle_directory,exist_ok=True)
    # Creating the CSV file to be written to
    f_csv = open(f'{o_scrape_helper.s_top_directory}scrape.csv', 'w', encoding = "utf-8")
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
    for i in range(i_pickles):
        o_page = pickle.load(open(f'{o_scrape_helper.s_pickle_directory}pickle{i}.p', 'rb'))
        for o_tweet in o_page:
            i_tweet_id = i_id
            i_id += 1
            s_created_at = o_tweet.created_at
            s_username = o_tweet.user.name
            s_screen_name = o_tweet.user.screen_name
            s_text = o_tweet.text
            i_reply_count = o_tweet.reply_count
            i_retweet_count = o_tweet.retweet_count
            i_likes = o_tweet.favorite_count
            s_location = o_tweet.place
            s_url = 'https://twitter.com/i/web/status/' + o_tweet.id_str

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

            # If retweet, set tweet equal to original tweet. This is because the retweeted tweet does not store media, but the original does
            if hasattr(o_tweet, "retweeted_status"):
                o_tweet = o_tweet.retweeted_status

            if hasattr(o_tweet, "extended_entities"):
                i_media_count = 1       # Integer, used to index media names should the tweet object have more than one
                # For each piece of media in extended entities
                for o_media in o_tweet.extended_entities["media"]:
                    # Find media type, build file name with associated type and ID, and save link to media in s_media_link
                    if (o_media['type'] == "photo"):
                        s_media_name = f"{o_scrape_helper.s_media_directory}photoID#{str(i_tweet_id).zfill(5)}-{str(i_media_count)}.jpg"
                        s_media_link = o_media['media_url_https']
                    elif (o_media['type'] == "video"):
                        s_media_name = f"{o_scrape_helper.s_media_directory}videoID#{str(i_tweet_id).zfill(5)}-{str(i_media_count)}.mp4"
                        s_media_link = o_media['video_info']['variants'][0]['url']
                    elif (o_media['type'] == "animated_gif"):
                       # Gif's are saved as .mp4's because that's how twitter stores them, as shown in the extended_entities object link above
                        s_media_name = f"{o_scrape_helper.s_media_directory}gifID#{str(i_tweet_id).zfill(5)}-{str(i_media_count)}.mp4"
                        s_media_link = o_media['video_info']['variants'][0]['url']

                    # Request s_media_link and download it's contents to s_media_name
                    o_request = requests.get(s_media_link)
                    with open(s_media_name, 'wb') as f_media:
                        f_media.write(o_request.content)

                    i_media_count += 1

o_scrape_helper = ScrapeHelper('griffin','twitter',l_hashtags=['eggs'])
v_query_full_archive_api(o_scrape_helper)
