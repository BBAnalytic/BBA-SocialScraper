"""
Created by: Griffin Fluet 
Created on: April 2021
Version: 1.0
Description: This file contains the ScrapeHelper class that will assist with the
scraping process by allowing access to essential variables needed for a scrape. 
"""
import tweepy
from datetime import datetime
from TwitterConfig import s_consumer_key, s_consumer_secret_key
from QueryBuilder import s_build_query

class ScrapeHelper:
    def __init__(self, s_user, s_platform, **kwargs):
        """
        """
        self.s_user = s_user
        self.s_platform = s_platform
        self.i_posts_scraped = 0
        if self.s_platform == 'twitter':
            self._v_make_api_connection()
            l_hashtags = kwargs.get('l_hashtags')
            l_locations = kwargs.get('l_locations')
            l_phrases = kwargs.get('l_phrases')
            self.s_query = s_build_query(l_hashtags, l_locations, l_phrases)
            if 's_from_date' in kwargs:
                self.s_from_date = kwargs.get('s_from_date')
            else:
                self.s_from_date = None
            if 's_to_date' in kwargs:
                self.s_to_date = kwargs.get('s_to_date')
            else:
                self.s_to_date = None
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
        s_now = datetime.now().strftime("%d-%m-%Y_%H.%M")
        self.s_top_directory = f'{o_user}_{s_now}/'
        self.s_media_directory = f'{self.s_top_directory}media/'

    def v_increment(self):
        """
        """
        self.i_posts_scraped =+ 1

    def i_get_posts_scraped(self):
        """
        """
        return self.i_posts_scraped
#to do add post counter, getter and setter
