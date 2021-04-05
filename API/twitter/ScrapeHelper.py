"""
Created by: Griffin Fluet 
Created on: April 2021
Version: 1.0
Description: This file contains the ScrapeHelper class that will assist with the
scraping process by allowing access to essential variables needed for a scrape. 
"""
import tweepy
from datetime import datetime
from twitter.TwitterConfig import s_consumer_key, s_consumer_secret_key
from twitter.QueryBuilder import s_build_query

class ScrapeHelper:
    def __init__(self, s_user, s_platform, **kwargs):
        """
        """
        self.s_user = s_user
        self.s_platform = s_platform
        if self.s_platform == 'twitter':
            self._v_make_api_connection()
            l_hashtags = kwargs.get('l_hashtags')
            l_locations = kwargs.get('l_locations')
            l_phrases = kwargs.get('l_phrases')
            s_from_date = kwargs.get('s_from_date')
            s_to_date = kwargs.get('s_to_date')
            if s_from_date != None:
                self.s_from_date = s_from_date
            if s_to_date != None:
                self.s_to_date = s_to_date
            self.s_query = s_build_query(l_hashtags, l_locations, l_phrases)
        else:
            # instagram setup will be done here
            pass
        self._v_set_working_directories(s_user)
        
    def _v_make_api_connection(self):
        """
        """
        o_auth = tweepy.AppAuthHandler(s_consumer_key,s_consumer_secret_key)
        o_api = tweepy.API(o_auth)
        self.o_api = o_api
        
    def _v_set_working_directories(self, o_user):
        """
        """
        s_now = datetime.now().strftime("%d-%m-%Y_%H")
        self.s_top_directory = f'./{o_user}_{s_now}/'
        if self.s_platform == 'twitter':
            self.s_pickle_directory = f'{self.s_top_directory}pickles/'
        self.s_media_directory = f'{self.s_top_directory}media/'
