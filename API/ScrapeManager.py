"""
"""
from ScrapeHelper import ScrapeHelper
from TweetExtractor import v_scrape_tweets_full_archive, v_scrape_tweets_thirty_day
import os, threading, time

# Dictionary of running threads
d_threads = {}

def _v_start_seven_day_scrape_twitter(o_scrape_helper,):
    """
    """

    # Zipping directory
    os.system(f'zip -rqq {o_scrape_helper.s_user}_{o_scrape_helper.s_platform}_scrape.zip {o_scrape_helper.s_top_directory}')
    # Removing the directory
    os.system(f'rm -rf {o_scrape_helper.s_top_directory}')
    # need to start scrape here
    # then zip directory and delete directory


def s_end_scrape(o_scrape_helper):
    pass
    # if called, need to stop scrape
    # once stopped, zip, and delete