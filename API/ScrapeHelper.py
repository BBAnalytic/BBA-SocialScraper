"""
Created by: Griffin Fluet 
Created on: April 2021
Version: 1.5
Description: This file contains the ScrapeHelper class that will assist with the
scraping process by allowing access to essential variables needed for a scrape. 
"""
import os, tweepy
from datetime import datetime
from TwitterConfig import s_consumer_key, s_consumer_secret_key
from QueryBuilder import s_build_query
from InstagramKeywordURLExtractor import b_url_extractor

class ScrapeHelper:
    def __init__(self, s_user, s_platform, **kwargs):
        """
        Init function for scrape helper class, takes in data passed in from the front end. Sets up 
        connection for twitters api, builds the queries for both instagram and twitter, and 
        creates working directories 

        Arguments: 
        - self - ScrapeHelper - the instance of the object
        - s_user - string - user's first bit of their email
        - s_platform - string - platform user is scraping
        - **kwargs - varying types - differing inputs for twitter and instagram
            twitter expects: 
                l_hashtags - list of hashtags
                l_locations - list of locations
                l_phrases - list of phrases
                s_from_date - string of from date, gets passed as MM/dd/yy
                s_to_date - string of to date, gets passed as MM/dd/yy
            instagram expects:
                s_search_term - string that is either single hashtag or a location url
                              - ex. '#blm' or 'www.instagram.com/explore/locations/498870164/new-delhi/'
                s_search_category - string of the category they are scraping either 'hashtag' or 'location'
        Output:
            No returned value but function results in a scrapehelper object ready to assist
            in scraping.
            Data stored in a Scrape Helper object:
                s_user - string containing user making scrape
                s_platform - string containing platform being scraped
                s_top_directory - string containing relative path to working directory of scrape
                s_media_directory - string containing relative path to media directory of scrape
                s_zip_name - string containt the name of the resulting zip file

                Twitter Data:
                o_api - API object containing connection for API
                s_query - string containing a query for API
                s_from_date - string containing a date to start searching from
                s_to_date - string containing a date to stop searching to

                Instagram Data:
                b_valid - boolean value whether URLExtractor successfully populated the url frontier            
        """
        self.s_user = s_user
        self.s_platform = s_platform

        # If platform is twitter, preform twitter setup
        if self.s_platform == 'twitter':
            self._v_make_api_connection()

            l_hashtags = kwargs.get('l_hashtags', None)
            l_locations = kwargs.get('l_locations', None)
            l_phrases = kwargs.get('l_phrases', None)
            self.s_query = s_build_query(l_hashtags, l_locations, l_phrases)

            s_unparsed_from_date = kwargs.get('s_from_date', None)
            s_unparsed_to_date = kwargs.get('s_to_date', None)
            self._v_parse_and_format_dates(s_unparsed_from_date, s_unparsed_to_date)


        # Otherwise it is instagram
        else:
            s_search_term = kwargs.get('s_search_term', None)
            s_search_category = kwargs.get('s_search_category', None)
            if s_search_category == 'hashtag':
                # Cannot pass a hashtag to instagram so have to remove
                s_search_term = s_search_term.replace('#','')
            self.s_search_term = s_search_term              # Instagram Search term
            self.s_search_category = s_search_category      # Instagram Search category
            
            self.b_valid = None                 # Bool weather Scrape was valid
            self.i_num_posts_wanted = 50        # Int Number of posts to be scraped from Instagram
            self.s_cookies = ''                 # String of cookies gathered from URlExtraction process

        self._v_name_working_directories(s_user)
        self.s_zip_name = f"{self.s_user}_{self.s_platform}_scrape.zip"
        
    def _v_make_api_connection(self):
        """
        Makes connection to Twitter API
        """
        o_auth = tweepy.AppAuthHandler(s_consumer_key,s_consumer_secret_key)
        o_api = tweepy.API(o_auth)
        self.o_api = o_api

    def _v_parse_and_format_dates(self, s_unparsed_from_date, s_unparsed_to_date):
        """
        Parses a yyyyMMddHHmm date from a dd/MM/yy date
        """
        # If dates are empty nothing needs to be done so return 
        if s_unparsed_from_date == '' and s_unparsed_to_date == '':
            return
        # Split dates by '/' to get a 3 element list ['MM','dd','yy']
        s_split_from_date = s_unparsed_from_date.split('/')
        s_split_to_date = s_unparsed_to_date.split('/')
        # Rebuilding the string but following yyyyMMddHHmm format, I add on the hours and minutes
        # 0000 gets added for from date and 2359 gets added for to date
        s_from_date = f'{s_split_from_date[2]}{s_split_from_date[0]}{s_split_from_date[1]}0000'
        s_HH_mm = datetime.now().strftime('%H%m')
        s_to_date = f'{s_split_to_date[2]}{s_split_to_date[0]}{s_split_to_date[1]}{s_HH_mm}'
        # Setting dates in scrape helper instance
        self.s_from_date = s_from_date
        self.s_to_date = s_to_date
        
    def _v_name_working_directories(self, o_user):
        """
        Creates the working directories of the scrape
        """
        s_now = datetime.now().strftime("%d-%m-%Y_%H.%M")
        self.s_top_directory = f'{o_user}_{s_now}/'
        self.s_media_directory = f'{self.s_top_directory}media/'

    def v_zip(self):
        """
        Zips the working directory at the end of the scrape and removes the top directory 
        """
        # Zipping directory
        os.system(f'zip -rqq {self.s_zip_name} {self.s_top_directory}')
        # Removing the directory
        os.system(f'rm -rf {self.s_top_directory}')