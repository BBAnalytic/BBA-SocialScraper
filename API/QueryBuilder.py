"""
Created by: Ryan Handlon
Created on: Feb 2021
Version: 1.0
Description: This file contains the function for building queries to pass into the api call.
"""

def s_build_query (l_hashtags=None, l_locations=None, l_phrases=None):
    """ 
    Query builder function, builds a query specifying the 
    types of tweets wished to be returned when query is passed to 
    a tweet search using the Twitter API. Function results in a 
    string being returned that is the built query.
    Info on query string being built can be found here:
    https://developer.twitter.com/en/docs/labs/recent-search/guides/search-queries

    No more than 10 total hashtags, locations, and phrases should be inputted.

    Arguments:
    - l_hashtags  - list   - a list of strings, the strings representing hashtags to be searched by
                           - strings should be in the format of "#hashtag" or "hashtag" 
                           - This is None by defalt
    - l_locations - list   - a list of strings, the strings representing locations to be searched by
                           - strings should be in the format of "New York" or ""New York"" 
                           - This is None by defalt
    - l_phrases   - list   - a list of strings, the strings representing phrases to be searched by
                           - strings should be in the format of "I hate Mondays!" or ""I hate Mondays!"" 
                           - This is None by defalt

    Output: 
    - s_query     - string - the query to be used to search tweets
                           - final query will look like "(#hashtag OR #hashtag) ("location" OR "location") ("phrase" OR "phrase")"
                    
    """

    s_query = ""      # String, holds query as it's being built

    # If there are hashtags to be added to query
    if (l_hashtags != None and l_hashtags != [""] and l_hashtags != []):
        s_query = s_query + "("
        # Iterate through each hashtag 
        for s_tag in l_hashtags:
            # Store original hashtag in case it needs do be formatted
            s_old_tag = s_tag
            # Add "#" in front of hashtag if not already there
            if (s_tag.find("#") != 0):
                s_tag = "#" + s_tag
            # If last hashtag add hashtag + ")", else add hashtag + " OR"
            if (l_hashtags.index(s_old_tag) == len(l_hashtags) - 1):
                s_query = s_query + s_tag + ") "
            else:
                s_query = s_query + s_tag + " OR "

    # If there are locations to be added to query
    if (l_locations != None and l_locations != [""] and l_locations != []):
        s_query = s_query + "("
        # iterate through each location 
        for s_loc in l_locations:
            s_old_loc = s_loc
            # Surround locations in quotes if not already there
            if not(s_loc.startswith("\"") and s_loc.endswith("\"")):
                s_loc = "\"" + s_loc + "\""
            # If last hashtag add hashtag + ")", else add hashtag + " OR"
            if (l_locations.index(s_old_loc) == len(l_locations) - 1):
                s_query = s_query + "place:" + s_loc + ") "
            else:
                s_query = s_query + "place:" + s_loc + " OR " 

    # If there are phrases to be added to query
    if (l_phrases != None and l_phrases != [""] and l_phrases != []):
        s_query = s_query + "("
        # Iterate through each phrase 
        for s_phrase in l_phrases:
            s_old_phrase = s_phrase
            # Surround phrase in quotes if not already there
            if not(s_phrase.startswith("\"") and s_phrase.endswith("\"")):
                s_phrase = "\"" + s_phrase + "\""
            # If last phrase add phrase + ")", else add phrase + " OR"
            if (l_phrases.index(s_old_phrase) == len(l_phrases) - 1):
                s_query = s_query + s_phrase + ") "
            else:
                s_query = s_query + s_phrase + " OR " 
    
    # Return query
    #s_query += ' -is:retweet'
    return s_query