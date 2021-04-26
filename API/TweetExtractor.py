"""
Created by: Griffin Fluet
Created on: Feb 2021
Version: 2.0
Description: This file contains three functions for scraping Twitter. Another for making the call to the 
api and scraping the data and getting to ready for archiving.
"""
import csv, os, re, requests, sys, tweepy
from TwitterConfig import s_full_dev_environment, i_full_search_pages, s_30_day_dev_environment, i_30_day_search_pages
from datetime import datetime
from ScrapeHelper import ScrapeHelper

def v_scrape_tweets_full_archive(o_scrape_helper):
    """ 
    Tweet scraper function, collects tweets from Twitter's API and scrapes 
    the text as well as the media of a tweet if it exists. Function results in a 
    zip archive containing a CSV file with scraped text along with a directory for 
    the media that was scraped. This function is for the full archive search

    Arguments:
    - o_scrape_helper - ScrapeHelper - Object that holds important data about the scrape
    being completed. See ScrapeHelper.py for more documentation

    Output: Function does not return a value.
    """

    # Creation of directories for scraped data
    os.makedirs(o_scrape_helper.s_media_directory,exist_ok=True)
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

    # Call to api made here, this returns a list of tweet objects
    # Checkout the attributes of a tweet object here: 
    # https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
    # Need to pass in the developer environment here to gain access to full archive
    # You can find more about the developer environment on the developer portal:
    # https://developer.twitter.com/en

    # List that will hold all tweets returned from API
    l_tweets = []

    # Since each API request can give a max of 500 tweets, 2 pages of results are requested
    # Each page will result in a request being used
    if(o_scrape_helper.s_from_date == '' and o_scrape_helper.s_to_date == ''): 
        for o_page in tweepy.Cursor(o_scrape_helper.o_api.search_full_archive,
                                    environment_name=s_full_dev_environment,
                                    query=o_scrape_helper.s_query,
                                    maxResults=500).pages(i_full_search_pages):
            l_tweets += o_page
    else: 
        for o_page in tweepy.Cursor(o_scrape_helper.o_api.search_full_archive,
                                    environment_name=s_full_dev_environment,
                                    query=o_scrape_helper.s_query,
                                    maxResults=500,
                                    fromDate=o_scrape_helper.s_from_date,
                                    toDate=o_scrape_helper.s_to_date).pages(i_full_search_pages):
            l_tweets += o_page


    # Using i as the iterative loop value and tweet id
    for i in range(len(l_tweets)):
        #json_str = json.dumps(l_tweets[i]._json)
        #parsed = json.loads(json_str)
        #print(json.dumps(parsed,indent=4,sort_keys=True))
        #print('\n')
        # Add 1 so counting is human like 
        i_tweet_id = i + 1
        s_created_at = l_tweets[i].created_at
        s_username = l_tweets[i].user.name
        s_screen_name = l_tweets[i].user.screen_name
        s_text = l_tweets[i].text
        i_reply_count = l_tweets[i].reply_count
        i_retweet_count = l_tweets[i].retweet_count
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
                    s_media_name = f"{o_scrape_helper.s_media_directory}photoID#{str(i_tweet_id).zfill(5)}-{str(i_media_count)}.jpg"
                    s_media_link = o_media['media_url_https']
                elif (o_media['type'] == "video"):
                    s_media_name = f"{o_scrape_helper.s_media_directory}videoID#{str(i_tweet_id).zfill(5)}-{str(i_media_count)}.mp4"
                    s_media_link = o_media['video_info']['variants'][0]['url']
                elif (o_media['type'] == "animated_gif"):
                    # Gif's are saved as .mp4's because that's how twitter stores them, as shown in the extended_entities object link above
                    s_media_name = f"{o_scrape_helper.s_media_directory}gifID#{str(i_tweet_id).zfill(5)}-{str(i_media_count)}.jpg"
                    s_media_link = o_media['video_info']['variants'][0]['url']

                # Request s_media_link and download it's contents to s_media_name
                o_request = requests.get(s_media_link)
                with open(s_media_name, 'wb') as f_media:
                    f_media.write(o_request.content)

                i_media_count += 1
    # Close csv 
    f_csv.close()
    # Archive scraped results
    o_scrape_helper.v_zip()

def v_scrape_tweets_30_day(o_scrape_helper):
    """ 
    Tweet scraper function, collects tweets from Twitter's API and scrapes 
    the text as well as the media of a tweet if it exists. Function results in a 
    zip archive containing a CSV file with scraped text along with a directory for 
    the media that was scraped. This function is for the 30 day search. Mostly used for testing purposes.

    Arguments:
    - o_scrape_helper - ScrapeHelper - Object that holds important data about the scrape
    being completed. See ScrapeHelper.py for more documentation

    Output: Function does not return a value.
    """
    
    # Creation of directories for scraped data
    os.makedirs(o_scrape_helper.s_media_directory,exist_ok=True)
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

    # Call to api made here, this returns a list of tweet objects
    # Checkout the attributes of a tweet object here: 
    # https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
    # Need to pass in the developer environment here to gain access to full archive
    # You can find more about the developer environment on the developer portal:
    # https://developer.twitter.com/en

    # List that will hold all tweets returned from API
    l_tweets = []

    # Since each API request can give a max of 100 tweets, 5 pages of results are requested
    # Each page will result in a request being used
    if(o_scrape_helper.s_from_date == '' and o_scrape_helper.s_to_date == ''): 
        for o_page in tweepy.Cursor(o_scrape_helper.o_api.search_30_day,
                                    environment_name=s_30_day_dev_environment,
                                    query=o_scrape_helper.s_query,
                                    maxResults=100).pages(i_30_day_search_pages):
            l_tweets += o_page
    else: 
        for o_page in tweepy.Cursor(o_scrape_helper.o_api.search_30_day,
                                    environment_name=s_30_day_dev_environment,
                                    query=o_scrape_helper.s_query,
                                    maxResults=100,
                                    fromDate=o_scrape_helper.s_from_date,
                                    toDate=o_scrape_helper.s_to_date).pages(i_30_day_search_pages):
            l_tweets += o_page

    # Using i as the iterative loop value and tweet id
    for i in range(len(l_tweets)):
        # Add 1 so counting is human like 
        i_tweet_id = i + 1
        s_created_at = l_tweets[i].created_at
        s_username = l_tweets[i].user.name
        s_screen_name = l_tweets[i].user.screen_name
        s_text = l_tweets[i].text
        i_reply_count = l_tweets[i].reply_count
        i_retweet_count = l_tweets[i].retweet_count
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
                    s_media_name = f"{o_scrape_helper.s_media_directory}photoID#{str(i_tweet_id).zfill(5)}-{str(i_media_count)}.jpg"
                    s_media_link = o_media['media_url_https']
                elif (o_media['type'] == "video"):
                    s_media_name = f"{o_scrape_helper.s_media_directory}videoID#{str(i_tweet_id).zfill(5)}-{str(i_media_count)}.mp4"
                    s_media_link = o_media['video_info']['variants'][0]['url']
                elif (o_media['type'] == "animated_gif"):
                    # Gif's are saved as .mp4's because that's how twitter stores them, as shown in the extended_entities object link above
                    s_media_name = f"{o_scrape_helper.s_media_directory}gifID#{str(i_tweet_id).zfill(5)}-{str(i_media_count)}.jpg"
                    s_media_link = o_media['video_info']['variants'][0]['url']

                # Request s_media_link and download it's contents to s_media_name
                o_request = requests.get(s_media_link)
                with open(s_media_name, 'wb') as f_media:
                    f_media.write(o_request.content)

                i_media_count += 1
    # Close csv 
    f_csv.close()
    # Archive scraped results
    o_scrape_helper.v_zip()


