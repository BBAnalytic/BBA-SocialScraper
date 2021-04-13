"""
"""
import threading
from twitter.TweetExtractorV2 import v_query_seven_day_api, v_query_full_archive_api, v_query_30_day_api
from twitter.ScrapeHelper import ScrapeHelper
import os, time

# Dictionary of running threads
d_threads = {}

def v_start_twitter_scrape(o_scrape_helper):
    o_thread = threading.Thread(target = _v_start_seven_day_scrape_twitter, args = (o_scrape_helper,) , daemon = True)
    d_threads = {o_scrape_helper.s_user : o_thread}
    o_thread.start
    

def _v_start_seven_day_scrape_twitter(o_scrape_helper,):
    """
    """
    print("ran")
    v_query_seven_day_api(o_scrape_helper)

    # Deleting pickles 
    os.system(f'rm -rf {o_scrape_helper.s_pickle_directory}')
    # Zipping directory
    os.system(f'zip -rqq {o_scrape_helper.s_user}_{o_scrape_helper.s_platform}_scrape.zip {o_scrape_helper.s_top_directory}')
    # Removing the directory
    os.system(f'rm -rf {o_scrape_helper.s_top_directory}')
    # need to start scrape here
    # once completed need to remove pickles
    # then zip directory and delete directory
    del d_threads[o_scrape_helper.s_user]
    o_thread.join


def s_start_30_day_scrape_twitter(o_scrape_helper):
    
    # Deleting pickles 
    os.system(f'rm -rf {o_scrape_helper.s_pickle_directory}')
    # Zipping directory
    os.system(f'zip -rqq {o_scrape_helper.s_user}_{o_scrape_helper.s_platform}_scrape.zip {o_scrape_helper.s_top_directory}')
    # Removing the directory
    os.system(f'rm -rf {o_scrape_helper.s_top_directory}')

def s_start_full_scrape_twitter(o_scrape_helper):
   

    # Deleting pickles 
    os.system(f'rm -rf {o_scrape_helper.s_pickle_directory}')
    # Zipping directory
    os.system(f'zip -rqq {o_scrape_helper.s_user}_{o_scrape_helper.s_platform}_scrape.zip {o_scrape_helper.s_top_directory}')
    # Removing the directory
    os.system(f'rm -rf {o_scrape_helper.s_top_directory}')
    # need to start scrape here
    # once completed need to remove pickles
    # then zip directory and delete directory

def s_end_scrape(o_scrape_helper):
    pass
    # if called, need to stop scrape
    # once stopped, remove pickles, zip, and delete


s_user = 'Griffin'
s_platform = 'twitter'
o_scrape_helper = ScrapeHelper(s_user,s_platform,l_hashtags=['eggs'])
v_start_twitter_scrape(o_scrape_helper)