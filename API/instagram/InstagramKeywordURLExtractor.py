"""
Created by: Ryan Handlon
Date Created: Feb 2021
Version: 1.0
Description: This file contains one function, which is used to build a frontier of posts to be scraped by navigate to instagram.com 
and scraping links off the explore page.
"""

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
from InstagramConfig import s_insta_username, s_insta_password, s_path_to_driver, d_headers

def v_url_extractor(s_search, i_num_posts_wanted = 100, s_category = 'hashtag'):
    """ InstagramURLExtractor - 
    
    Scrapes links to instagram posts of the internet using selenium and compiles them into a text document 
    titled "URLFrontier.txt".

    Arguments:
    - s_search   - string  - search term that is being scraped, whether its a hashtag or location
                           - if scraping a hashtag, don't include the # - example: "blm"
                           - if scraping a location, this must be the link to a location explore page on instagram 
                           - example: "www.instagram.com/explore/locations/498870164/new-delhi/"
    - i_posts    - integer - number of posts to be scraped
                           - this feature is currently here temporarily and will be removed later.
                           - default i_posts is 100
    - s_category - string  - what type of search is being done "hashtag" or "location"
                           - default s_category is "hashtag"

    Output: 
        The function does not return anything, but does create a text document titled "URLFrontier.txt"
        which contains all of the links that were scraped, each link appearing on it's own line in the text file
    """

    i_window_width = 1920     # Width of headless chrome window in pixles
    i_window_height = 1080    # Height of headless chrome window in pixles
    i_wait = 5                # Number of seconds to implicitly wait
    i_scroll_pixels = 1080    # Number of pixels to scroll down
    l_links_to_posts = []     # List of links being scraped

    # Build link to explore page based of if searching hashtag or location
    if(s_category == 'hashtag'):
        s_explore_page = 'https://www.instagram.com/explore/tags/' + s_search + '/'
    elif (s_category == 'location'):
        s_explore_page = s_search

    # Building a regex used to match instaggram links to posts 
    re_valid_link = re.compile(r'(https:\/\/www\.instagram\.com\/p\/)(\w|_){11}(\/)')

    # Setting chromebrowser to headless, disabling gpu, and setting a manuel useragent so instagram doesn't detect selenium is running headless
    o_browser_options = Options()
    o_browser_options.add_argument(f"--window-size={i_window_width},{i_window_height}")
    o_browser_options.add_argument("--headless")
    o_browser_options.add_argument("--disable-gpu")

    # The useragent in InstagramConfig must be for Google Chrome and the operating system  this script is running on  
    o_browser_options.add_argument(d_headers['user-agent'])

    # Load Chromedriver
    o_browser = webdriver.Chrome(executable_path = s_path_to_driver, options = o_browser_options)
    # Set implicitly wait value, forcing selenium to wait an alloted time before throwing errors 
    o_browser.implicitly_wait(i_wait)

    # Load Instagram.com
    o_browser.get('https://www.instagram.com/')

    # Locate username and password text boxes
    o_username_input = o_browser.find_element(By.CSS_SELECTOR, "input[name='username']")
    o_password_input = o_browser.find_element(By.CSS_SELECTOR, "input[name='password']")

    # Input username and password
    o_username_input.send_keys(s_insta_username)
    o_password_input.send_keys(s_insta_password)

    # Find login button and click it
    o_login_button = o_browser.find_element_by_xpath("//button[@type='submit']")
    o_login_button.click()

    # This should only be here temporarily. Is needed so an error isn't thrown.
    # Need to find a way to wait till page is loaded
    sleep(5)

    # Load explore page to be scraped
    o_browser.get(s_explore_page)

    i_last_iteration_num_scraped_posts = 0
    i_iterations_with_no_scrape = 0
    i_num_scraped_posts = 0
    # Iterate till requested # of posts scraped
    while(i_num_scraped_posts < i_num_posts_wanted):
        # Scroll down page by i_scroll_pixles and grab all links on page
        o_browser.execute_script("window.scrollBy(0, " + str(i_scroll_pixels) + ")")

        l_explore_links = o_browser.find_elements_by_xpath("//a[@href]")

        # Sometimes theres an error where the page hasn't loaded yet, if so just pass for next iteration
        try:
            # For each link, if its a link to a post and not been scraped yet, add it to the list
            for o_explore_link in l_explore_links:
                if o_explore_link.get_attribute("href") not in l_links_to_posts and re_valid_link.match(o_explore_link.get_attribute("href")) != None:
                    l_links_to_posts.append(o_explore_link.get_attribute("href"))
                    i_num_scraped_posts += 1
                    i_iterations_with_no_scrape = 0
            # If it has not scraped new links in 50 iterations break, else update variables
            if i_num_scraped_posts == i_last_iteration_num_scraped_posts and i_iterations_with_no_scrape == 50:
                break
            elif i_last_iteration_num_scraped_posts == i_num_scraped_posts:
                i_iterations_with_no_scrape += 1
            else:
                i_last_iteration_num_scraped_posts = i_num_scraped_posts
        except:
            pass

    # Write scraped post links to URLFrontier text document
    f_frontier = open("URLFrontier.txt", "w", encoding= 'utf-8')
    for s_link in l_links_to_posts:   
        f_frontier.write(s_link + "\n")

    # Close f_frontier and O_browser
    f_frontier.close()
    o_browser.close()
