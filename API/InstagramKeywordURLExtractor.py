"""
Created by: Ryan Handlon
Date Created: Feb 2021
Version: 2.0
Description: This file contains one function, which is used to build a frontier of posts to be scraped by navigate to instagram.com 
and scraping links off the explore page.
"""

import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import re
from InstagramConfig import s_path_to_driver, d_headers, d_login_dict



def b_url_extractor(s_search, i_num_posts_wanted = 50, s_category = 'hashtag'):
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
        The function returns a boolean value. If False is returned, that means there was invalid input 
        and the scrape couldn't finish, usually because there is no instagram page associated with the input. 
        If True is returned, that means there was valid input for the scrape. The function also creates a 
        text document titled "URLFrontier.txt" which contains all of the links that were scraped, each 
        link appearing on it's own line in the text file
    """

    i_window_width = 1920     # Width of headless chrome window in pixles
    i_window_height = 1080    # Height of headless chrome window in pixles
    i_wait = 5                # Number of seconds to implicitly wait
    i_scroll_pixels = 1080    # Number of pixels to scroll down


    # Build link to explore page based of if searching hashtag or location
    if(s_category == 'hashtag'):
        s_explore_page = 'https://www.instagram.com/explore/tags/' + s_search + '/'
    elif (s_category == 'location'):
        # Regex for location link triming off everything after number in link
        # If match, set equal to s_explore_page, else return false
        re_valid_location = re.compile(r'(https:\/\/www\.instagram\.com\/explore\/locations\/)(\d)+').match(s_search)
        if re_valid_location:
            s_explore_page = re_valid_location.group(0)
        else:
            return False
    else:
        # Bad input, return False
        return False

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


    i_passwd_index = random.randint(0, len(d_login_dict.keys())-1)     # Randomly chosen password index from login dictionary 
    i_original_index = i_passwd_index                                  # Original value of password index
    b_logged_in = False                                                # Boolean if we've logged into Instagram

    # While not logged in
    while(b_logged_in == False):

        # Load Instagram.com
        o_browser.get('https://www.instagram.com/')

        # Locate username and password text boxes
        o_username_input = o_browser.find_element(By.CSS_SELECTOR, "input[name='username']")
        o_password_input = o_browser.find_element(By.CSS_SELECTOR, "input[name='password']")

        # Input username and password
        o_username_input.send_keys(list(d_login_dict.keys())[i_passwd_index])
        o_password_input.send_keys(d_login_dict[list(d_login_dict.keys())[i_passwd_index]])

        # Find login button and click it
        o_login_button = o_browser.find_element_by_xpath("//button[@type='submit']")
        o_login_button.click()

        # This while loop tests to make sure the page has loaded before proceding
        # If page doesn't get loaded, program ends up leaving the page before login in, causing problems later.
        # While true, keep testing to find search box on page, once found set logged in to True and break from loop
        # If login error gets found first, break from inner loop so outer loop can start over
        i_delay = 0         # Delay of WebDriverWait calls in seconds
        while (True):
            try:
                WebDriverWait(o_browser, i_delay).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']")))
                b_logged_in = True
                break
            except TimeoutException:
                try:
                    WebDriverWait(o_browser, i_delay).until(EC.presence_of_element_located((By.XPATH, "//p[@data-testid='login-error-message']")))
                    break
                except TimeoutException:
                    pass
        # Increment i_passwd_index
        i_passwd_index += 1
        
        # If i_passwd_index = length of dictionary, set it to 0
        if(i_passwd_index == len(d_login_dict.keys())):
            i_passwd_index = 0
        
        # If we've looped back to original index, all accounts are banned, return False
        if(i_passwd_index == i_original_index):
            return False

    # Load explore page to be scraped
    o_browser.get(s_explore_page)

    # Try to find "Sorry, this page isn't available."
    # If found, bad input, return False
    try:
        s_bad_page = o_browser.find_element(By.CLASS_NAME, "_7UhW9").text
        if(s_bad_page == "Sorry, this page isn't available."):
            return False
    except NoSuchElementException:
        pass

    # Grab number of posts from explore page if it's there
    try:
        # g47SY is the class name of div that holds number of posts on page
        i_post_count = int(o_browser.find_element(By.CLASS_NAME, "g47SY").text.replace(',',''))
    except NoSuchElementException:
        # Just set to a really high number that'll never be reached
        i_post_count = 10000000000

    l_post_buffer = []         # Buffer of the past 15 posts scraped to make sure we don't scrape duplicates
    i_num_scraped_posts = 0    # Number of posts that have been scrped
    i_buffer_size = 15         # Size of post buffer to make sure we're not rescraping links
    b_not_bottom = True        # Is browser at bottom of page
    i_old_height = 0           # last iteration height of browser

    #Open URLFrontier file
    f_frontier = open("URLFrontier.txt", "w", encoding= 'utf-8')

    # add escape if global variable ticked into this logic, eventually remove i_num_posts_wanted
    # While number of scraped posts is less than number of posts wanted and number of posts on page and not at bottom of page
    while(i_num_scraped_posts < i_post_count and i_num_scraped_posts < i_num_posts_wanted and b_not_bottom):
        l_explore_links = o_browser.find_elements_by_xpath("//a[@href]")

        # Try catch because sometimes posts haven't loaded yet 
        try:
            # For each link on page
            for o_explore_link in l_explore_links:
                # If link not in buffer and matches regex
                if o_explore_link.get_attribute("href") not in l_post_buffer and re_valid_link.fullmatch(o_explore_link.get_attribute("href")) != None:
                    # If buffer not full, add link to buffer
                    if(len(l_post_buffer) < i_buffer_size):
                        l_post_buffer.append(o_explore_link.get_attribute("href"))
                    # If buffer full, remove oldest link, add newest link to buffer
                    elif (len(l_post_buffer) == i_buffer_size):
                        l_post_buffer.append(o_explore_link.get_attribute("href"))
                        l_post_buffer.pop(0)

                    # Write link to frontier, increment i_num_scraped_posts
                    f_frontier.write(o_explore_link.get_attribute("href") + "\n")
                    i_num_scraped_posts += 1

        # If we did get an error, just pass, hopefully page has loaded by next iteration
        except:
            pass

        if (s_category == 'location'):
            i_height = o_browser.execute_script("return document.body.scrollHeight")  # Current browser height

            # Try to find loading div on page
            try:
                # By4na is class name of div with loading text in it
                WebDriverWait(o_browser, i_delay).until(EC.visibility_of_element_located((By.CLASS_NAME, "By4nA")))

            # If load div not found and page height hasn't changed, set bottom of page to true
            except TimeoutException:
                if(i_old_height == i_height):
                    b_not_bottom = False
                i_old_height = i_height
        
        # Scroll page down
        o_browser.execute_script("window.scrollBy(0, " + str(i_scroll_pixels) + ")")

    # Close f_frontier and o_browser
    f_frontier.close()
    o_browser.close()
    return True