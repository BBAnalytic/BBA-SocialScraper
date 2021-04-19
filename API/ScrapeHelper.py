"""
Created by: Griffin Fluet 
Created on: April 2021
Version: 1.0
Description: This file contains the ScrapeHelper class that will assist with the
scraping process by allowing access to essential variables needed for a scrape. 
"""
import os, tweepy
from datetime import datetime, timedelta
from TwitterConfig import s_consumer_key, s_consumer_secret_key
from QueryBuilder import s_build_query
from InstagramKeywordURLExtractor import b_url_extractor

class ScrapeHelper:
    def __init__(self, s_user, s_platform, **kwargs):
        """
        """
        self.s_user = s_user
        self.s_platform = s_platform
        self.i_posts_scraped = 0

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
                s_search_term = s_search_term.replace('#','')
            s_search_term = s_search_term
            s_search_category = s_search_category
            self.b_valid = b_url_extractor(s_search_term, s_category=s_search_category)

        self._v_set_working_directories(s_user)
        self.s_zip_name = f"{self.s_user}_{self.s_platform}_scrape.zip"
        
    def _v_make_api_connection(self):
        """
        """
        o_auth = tweepy.AppAuthHandler(s_consumer_key,s_consumer_secret_key)
        o_api = tweepy.API(o_auth)
        self.o_api = o_api

    def _v_parse_and_format_dates(self, s_unparsed_from_date, s_unparsed_to_date):
        """
        """
        # If dates are empty nothing needs to be done so return 
        if s_unparsed_from_date == '' and s_unparsed_to_date == '':
            return
        # Split dates by '/' to get a 3 element list ['dd','MM','yy']
        s_from_date = s_unparsed_from_date.split('/')
        s_to_date = s_unparsed_to_date.split('/')
        # Adding leading 20 to year 
        s_from_date[2] = f'20{s_from_date[2]}'
        s_to_date[2] = f'20{s_from_date[2]}'
        # Rebuilding the string
        


    def _v_set_working_directories(self, o_user):
        """
        """
        s_now = datetime.now().strftime("%d-%m-%Y_%H.%M")
        self.s_top_directory = f'{o_user}_{s_now}/'
        self.s_media_directory = f'{self.s_top_directory}media/'

    def v_zip(self):
        """
        """
        # Zipping directory
        os.system(f'zip -rqq {self.s_zip_name} {self.s_top_directory}')
        # Removing the directory
        os.system(f'rm -rf {self.s_top_directory}')