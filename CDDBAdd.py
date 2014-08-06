"""
CDDB Fast Add Tool.
@author <scj7t4@mst.edu>
PUBLIC DOMAIN
"""

import os
import sys
import json
import unicodedata
from urllib import urlencode
import webbrowser
import traceback
import re
import exceptions

import discid
import musicbrainzngs

DEBUG = False
KLAP_URL = "http://klap.kmnr.org/lib/json/"

def normalize(itm):
    """
    This function removes all the funny characters and downcodes them to an
    ascii equivalent.
    """
    return unicodedata.normalize('NFKD', itm).encode('ascii', 'ignore')

def normalize_list(lst):
    """
    Calls normalize on a list of strings.
    """
    return [ normalize(x) for x in lst ]

def choose_option(option_lst):
    """
    Prints a menu of strings, lets the user pick one as a number (or a manual
    entry option, and returns the string the user selected
    """
    final_lst = list(set(option_lst))
    while 1:
        c = 1
        for item in final_lst:
            print "{}) {}".format(c,item)
            c += 1
        print "{}) Manually Set".format(c)
        try:
            choice = int(raw_input("Your Choice: "))
        except ValueError:
            print "You have to enter a number"
            continue
        if 0 < choice <= len(final_lst):
            return final_lst[choice-1]
        elif choice == len(final_lst)+1:
            inp = str(raw_input("Manual Value: "))
            inp = inp.strip()
            return inp
        else:
            print "Invalid Choice"
            continue

def wait_and_exit(msg,code=1):
    """
    Prints an error message. Waits to sys.exit program until user presses enter.
    """
    print msg
    raw_input("Press ENTER to continue")
    sys.exit(code)
            
def main():
    """
    Scans a folder for music files with metadata. Collects metadata information
    from all music files and assumes they belong to the same album. Produces a
    simple description of the album that it loads into a KLAP form.
    """
    
    # Help the user
    if len(sys.argv) != 2:
        print "Usage: {} Drive".format(sys.argv[0])
        sys.exit(1)

    tracks = []
    musicbrainzngs.set_useragent("KLAP-CDDBAdd", "0.1", "engineering@kmnr.org")

    disc = discid.read(sys.argv[1])
    try:
        result = musicbrainzngs.get_releases_by_discid(disc.id,
                                                       includes=["artists","recordings"])
    except musicbrainzngs.ResponseError:
        wait_and_exit("Couldn't find that disc in the online database, sorry!")
    else:
        if result.get("disc"):
            artist = result["disc"]["release-list"][0]["artist-credit-phrase"]
            album = result["disc"]["release-list"][0]["title"]
            dk = "disc"
        elif result.get("cdstub"):
            artist = result["cdstub"]["artist"]
            album = result["cdstub"]["title"]
            dk = "cdstub"
        for track in result[dk]['release-list'][0]['medium-list'][0]['track-list']:
            title = track['recording']['title']    
            d = {'number': int(track['position']),
                 'title': title}
            tracks.append(d)
    
    # Make sure the info is safe for KLAP
    artist = artist
    album = album
    
    print "\n-----------------------------\n"
    
    # Make the dict
    obj = {'artist': artist,
           'album': album,
           'tracks': tracks,
          }

    # Code it as json
    js = json.dumps(obj)
    # Make a query string dict
    dic = {'data':js}
    # Encode it as a query string
    qs = urlencode(dic)
    # Determine target url
    final_url = "{}?{}".format(KLAP_URL,qs)
    # Open up KLAP!
    webbrowser.open_new_tab(final_url)

if __name__ == "__main__":
    try:
        main()
    except exceptions.SystemExit:
        raise
    except:
        print "Unexpected error:", sys.exc_info()[0]
        traceback.print_exc()
        wait_and_exit("Please take a screenshot and e-mail it to engineering@kmnr.org")