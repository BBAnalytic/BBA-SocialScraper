"""
Created by: Griffin Fluet
Date Created: Feb 2021
Version: 1.0
Description: This file contains two functions. The first function is a thread 
worker function used to scrape posts on instagram. The second fills a thread safe 
queue with the links from the url frontier.
"""
import csv, os, threading
from InstagramConfig import d_headers
from queue import Queue
from instascrape import Post
from time import sleep
from datetime import datetime

def _v_scrape_post(q_url, l_counter=[0]):
    """ 
    Post scraper worker function, each worker will scrape an Instagram 
    post, write data to csv file, and download visual media.  

    Arguments:
    - q_url - Queue - reference to queue holding instagram post links
    - l_counter - list<int> - keeping track of number of posts scraped 
        to generate ids

    Output:
    Function does not return a value.
    """

    while True:
        s_url = q_url.get()
        o_post = Post(s_url)
        o_post.scrape(headers=d_headers)
        s_timestamp = o_post.timestamp
        s_full_name = o_post.full_name
        s_username = o_post.username
        s_caption = o_post.caption
        s_likes = o_post.likes
        s_location = o_post.location

        # Waits here until able to write to file
        while o_global_lock.locked():
            continue

        # Thread gains access to write to file
        o_global_lock.acquire()

        # Increment counter before writing to csv file
        l_counter[0] += 1
        s_post_id = str(l_counter[0]).zfill(5)

        o_writer.writerow({
            'Post ID' : s_post_id,
            'Timestamp' : s_timestamp,
            'Full Name' : s_full_name,
            'Username' : s_username,
            'Caption' : s_caption,
            'Likes' : s_likes,
            'Location' : s_location,
            'Link' : s_url})
        # Then releases lock once done
        o_global_lock.release()

        # Checks media type to ensure corrent naming and extension 
        if o_post.is_video:
            o_post.download(f'{s_media_directory}videoID#{s_post_id}.mp4')
        else:
            o_post.download(f'{s_media_directory}pictureID#{s_post_id}.jpg')

        # Let queue know task is done
        q_url.task_done()

# Setting up directories for scraped data
s_now = datetime.now().strftime("%d-%m-%Y_%H")
s_main_directory = f'./{s_now}/'
s_media_directory = f'{s_main_directory}media/'
os.makedirs(s_media_directory,exist_ok=True)
# Creating the CSV file to be written to
f_csv = open(f'{s_main_directory}scrape.csv', 'w', encoding='utf-8')
# Setting fields for csv format
l_fields = [
    'Post ID',
    'Timestamp',
    'Full Name',
    'Username',
    'Caption',
    'Likes',
    'Location',
    'Link']
# Object to write to csv file
o_writer = csv.DictWriter(f_csv,dialect='excel',fieldnames=l_fields)
o_writer.writeheader()
# Lock for threads writing to file, this ensures only one writing at a time
o_global_lock = threading.Lock()
# Used for serializing posts
l_counter = [0]
# Threadsafe queue for holding in instagram links
q_url = Queue(maxsize=0)

# Creating five threads
for i in range(5):
    o_thread = threading.Thread(target=_v_scrape_post, args=(q_url,))
    o_thread.setDaemon(True)
    o_thread.start()

def v_read_to_queue():
    """ 
    Fills queue with links from URLFrontier. Reads frontier line by line
    into the queue.

    Arguments:
    None

    Output: 
    Function does not have a return value. 

    """
    # Reading in urls from frontier
    f_url_frontier = open("URLFrontier.txt","r")
    s_url = f_url_frontier.readline()
    # While there are still urls left to read, add them to queue
    while s_url:
        q_url.put(s_url)
        s_url = f_url_frontier.readline()
    f_url_frontier.close()
    q_url.join()