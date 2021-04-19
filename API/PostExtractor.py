"""
Created by: Griffin Fluet
Date Created: Feb 2021
Version: 2.0
Description: Need to update this
"""
import csv, os
from InstagramConfig import d_headers
from instascrape import Post
from instascrape.exceptions.exceptions import InstagramLoginRedirectError
from ScrapeHelper import ScrapeHelper

def v_scrape_instagram(o_scrape_helper):
    """
    """
    # Creation of directories for scraped data
    os.makedirs(o_scrape_helper.s_media_directory,exist_ok=True)
    # Creating the CSV file to be written to
    f_csv = open(f'{o_scrape_helper.s_top_directory}scrape.csv', 'w', encoding = "utf-8")
    # Setting fields for csv formatting
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
    # Writing headers of csv file
    o_writer.writeheader()

    # Reading in urls from frontier
    f_url_frontier = open("URLFrontier.txt","r")
    s_url = f_url_frontier.readline()
    i_post_count = 1

    while s_url:
        try:
            o_post = Post(s_url)
            o_post.scrape(headers=d_headers)
            s_timestamp = o_post.timestamp
            s_full_name = o_post.full_name
            s_username = o_post.username
            s_caption = o_post.caption
            s_likes = o_post.likes
            s_location = o_post.location

            o_writer.writerow({
                'Post ID' : i_post_count,
                'Timestamp' : s_timestamp,
                'Full Name' : s_full_name,
                'Username' : s_username,
                'Caption' : s_caption,
                'Likes' : s_likes,
                'Location' : s_location,
                'Link' : s_url})
        
            if o_post.is_video:
                o_post.download(f'{o_scrape_helper.s_media_directory}videoID#{str(i_post_count).zfill(5)}.mp4')
            else:
                o_post.download(f'{o_scrape_helper.s_media_directory}pictureID#{str(i_post_count).zfill(5)}.jpg')
        
            i_post_count += 1
        except InstagramLoginRedirectError:
            pass
        finally:
            s_url = f_url_frontier.readline()

    f_url_frontier.close()
    o_scrape_helper.v_zip()


#s_user = 'Ryan'
#s_search_term = 'https://www.instagram.com/explore/locations/222655914/washington-dc-nations-capitol/'
#s_search_category = 'location'
#o_scrape_helper = ScrapeHelper(s_user, 'instagram', s_search_term=s_search_term, s_search_category=s_search_category)
#v_scrape_instagram(o_scrape_helper)