"""
"""
from concurrent.futures import ThreadPoolExecutor
from twitter.TweetExtractorV2 import v_query_seven_day_api, v_query_full_archive_api
from twitter.ScrapeHelper import ScrapeHelper
import os, time

o_executor = ThreadPoolExecutor(10)
# Dictionary of running threads
d_threads = {}

def s_start_seven_day_scrape_twitter(o_scrape_helper):
    o_future = o_executor.submit(v_query_seven_day_api, o_scrape_helper)
    d_threads[o_scrape_helper.s_user] = o_future
    while o_future.done() != True or o_future.cancelled():
        continue
    del d_threads[o_scrape_helper.s_user]

    # Deleting pickles 
    os.system(f'rm -rf {o_scrape_helper.s_pickle_directory}')
    # Zipping directory
    os.system(f'zip -rqq {o_scrape_helper.s_user}_{o_scrape_helper.s_platform}_scrape.zip {o_scrape_helper.s_top_directory}')
    # Removing the directory
    os.system(f'rm -rf {o_scrape_helper.s_top_directory}')
    # need to start scrape here
    # once completed need to remove pickles
    # then zip directory and delete directory

def s_start_full_scrape_twitter(o_scrape_helper):
    o_future = o_executor.submit(v_query_full_archive_api, o_scrape_helper)
    d_threads[o_scrape_helper.s_user] = o_future
    while o_future.done() != True or o_future.cancelled():
        continue
    del d_threads[o_scrape_helper.s_user]

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
s_start_seven_day_scrape_twitter(o_scrape_helper)
s_user = 'Niffirg'
o_scrape_helper = ScrapeHelper(s_user,s_platform,l_hashtags=['bacon'])
#s_start_full_scrape_twitter(o_scrape_helper)