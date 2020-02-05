'''a script which scrapes a user's reviews given user ID number, a simple int from 1 to over 100m, each a unique goodreads user ID'''

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions as seleniumerrors
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)

import numpy as np

import time
import json

from pymongo import MongoClient

import pprint

import bs4
from bs4 import BeautifulSoup

import re
import numpy as np

import spacy
from spacy_langdetect import LanguageDetector


def remove_text_inside_brackets(text, brackets="<>"):
    count = [0] * (len(brackets) // 2) # count open/close brackets
    saved_chars = []
    for character in text:
        for i, b in enumerate(brackets):
            if character == b: # found bracket
                kind, is_close = divmod(i, 2)
                count[kind] += (-1)**is_close # `+1`: open, `-1`: close
                if count[kind] < 0: # unbalanced bracket
                    count[kind] = 0  # keep it
                else:  # found bracket to remove
                    break
        else: # character is not a [balanced] bracket
            if not any(count): # outside brackets
                saved_chars.append(character)
    return ''.join(saved_chars)


def get_lang(words, nlp):
    if len(words)<4:
        lang = -1
    else:
        doc = nlp(words)
        lang = doc._.language['language']
    
    return lang

def get_text(readable):
    try:
        l = readable[0].contents # turns out there's only one readable in each review. Pretty good so far. 
    except:
        return -1
    freetextlst = [s for s in l if "freeText" in str(s)] 

    #rev_text = ' '.join(map(str, freetextlst)) includes the freetext and freetext containers, and that is..troublesome
    rev_text = str(freetextlst[-1])
    # bigstring = seperator.join(strlchildren)
    review_nlp_document = remove_text_inside_brackets(rev_text)
    
    return review_nlp_document

def str_to_rate(qual_state):
    '''
    a function that turns goodreads's "I liked it" or "I did not like it" star categories
    into the numerical 1-5 rating that they visually imply. 
    ++++++
    Attributes
    qual_state (list) a split string pulled from the beautiful soup output of .text on the rating object
    ++++++
    Returns
    user_rating (int): 1-5 score based on NUMBER OF STARS SELECTED BY THE RATER. I honestly don't understand why that's not the output in the HTML. 
    '''
    if qual_state[-3:] == ['it', 'was', 'amazing']:
        user_rating = 5
    elif qual_state[-3:] ==['really','liked','it']:
        user_rating = 4
    elif qual_state[-2:] ==['liked', 'it']:
        '''note that I belive any that include "really" will be given 4
        before we get to this elif statement, therefore we don't need 
        to worry about the issues of "really liked it" and "liked it"
        overlapping'''
        user_rating= 3
    elif qual_state[-3:]==['it','was','ok']:
        user_rating = 2
    elif qual_state[-3:]==['not','like','it']:
        user_rating = 1
    else:
        user_rating = 0
    return user_rating


def save_to_mongo(add_this, db, collection):
    '''
    Helperfunction that takes a list of reviews, appends them to dictonaries, and feeds them into mongodb
    
    Attributes:
    add_this (dict): dictonary to add to mongo
    db (str): specific string of the db to use
    collection (str): string of the collection
    '''
    #connect to the mongo thing
    client = MongoClient()
    db = client['reveiws']
    collection = db['clean']
    print(add_this)
    db.collection.insert_one(add_this) 
    #add doc to mongodb
    client.close()



#hacky way to easily edit the range to operate over in nano on the ec2
#start, stop = 4667023, 4667025


def click_in_margin():
    '''gets rid of an annoying pop-up that asks you to log in whenever you load a page'''
    actions.move_by_offset(25,150).click().perform()
    actions.move_by_offset(-25,-150).perform()
    

def scroll_to_bottom(scroll_wait):
    '''a function which rolls through a page to force the lazy loader to load everything'''
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        time.sleep(scroll_wait) #wait for page to load
        
        last_height = new_height

def scoop_reviews():
    '''
    a function to take the page of reviews and turn it into jsons

    Attributes:
    None

    Returns:
    jsons: list of jsons
    
    '''
    # pull all class objects called 'bookalike review' into a list 
    try:
        
        reviews = driver.find_elements_by_class_name("friendReviews")
        
    except:
        print ('that book had no reviews')
        pass
    #turn the bookalikes into json lists
    print(str(len(reviews))+' got that many reviews')
    #for elements in reviews:
     #   print(str(elements)[:20]) #hash this out, testing
    jsons = [items.get_attribute('outerHTML') for items in reviews]
        
    return jsons

def each_page():
    '''
    helper function that will go to the next page in the reviews page.
    
    Attributes:
    None
    
    Returns:
    dicontary: book_id : list of reviews
    '''
    docs = []
    pages = 0
    while True:
        print('letting this load')
        
        time.sleep(2)
        new_doc =scoop_reviews()
        for i in new_doc:
            #print(i[:90])
            docs.append(i)
        
        try:
            elm = driver.find_element_by_class_name('next_page')
            print('getting the next ten reviews')
            pages +=1
            elm.click()
        except (seleniumerrors.NoSuchElementException, seleniumerrors.ElementClickInterceptedException):
            print("this book didn't have more than one page of reviews")
            return docs # stops looking and returns docs if this book doesn't have more pages. 
        time.sleep(1)
        

        try:
            elm= driver.find_element_by_class_name('next_page')
            if 'disabled' in elm.get_attribute('class'):
                print('I got to the end of these pages!')
                return docs
        except:
            print('got {} pages of reviews from this book!'.format(pages))

            return docs
        
        print('going to next page!')
        
    print('got {} pages of reviews from this book!'.format(pages))
    return docs


def log_current_sample():
    '''
    a simple helperfunction that keeps track of where in the sampling order we are
    ++++++++++
    Attributes
    None    
    ++++++++++
    Returns
    None    
    '''
    with open('progress.txt', 'w')as f:
        f.write(str(samples[current_index]))

def import_samples():
    '''
    takes the list of samples and turns them into a workable list
    ++++++++++
    Attributes
    None
    ++++++++++
    Returns
    the list of sample goodreads user ids generated by random sampling
    '''

    samples = np.loadtxt('samples.txt')
    return [int(items) for items in samples]


def get_next_page(book_id):
    '''moves to the next page according to the samples
    ++++++++++
    Attributes
    
    ++++++++++
    Returns
    book_id: (int) the userid from samples
        
    '''
    
    ratings_url = 'https://www.goodreads.com/book/show/{}'.format(book_id)
    print('trying to load '+ratings_url)
    driver.get(ratings_url)
    

def get_last_index():
    '''
    checks our progress for system restarts
    ++++++++++
    Attributes
    None
    ++++++++++
    Returns
    the index of the most recent sample pulled from goodreads
    '''
    progress = int(np.loadtxt('progress.txt'))
    print ('{} is in the progress log'.format(progress))
    
    return samples.index(progress)

def clean_one(add_this,nlp):

    ''' 
    function which will use the scraper to update the mongo with properly cleaned stuff, so the scraper can clean and scrape (yay!)
    +++++++++++
    Attributes:
    add_this (dict): dictonary of items to add to the mongo
    +++++++++++
    Returns:
    Nothing
    '''
   

    client = MongoClient('localhost', 27017)
    db=client['reviews'] ## Get all the mongo stuff up and running
    coll=db['cleaned']
    soup = BeautifulSoup(add_this, 'html.parser')
    readable = soup.find_all(class_ = "readable")
    
    
    nlp_words = get_text(readable)
    if nlp_words == -1:
        return('no text here')

    language = get_lang(nlp_words, nlp)
    try: #some people are leaving reviews without giving the books any stars. interesting. 
        rate_string = soup.find_all(class_ = re.compile('staticStars notranslate'))[0].attrs['title']
        rate = str_to_rate(rate_string.split())
    except IndexError:
        rate = -1
    
    try: #catching the documents with nothing in them. 
        title = soup.find_all(class_ = re.compile('lightGreyText'))[0].attrs['title'], ##title is likely to produce borked results. this one is just an isbn. soo..yeah
    except IndexError:
        title = -1
        
        
    
    formatted_dct = {'book_id' : int(book_id),
                    'nlp_words' : get_text(readable),
                    'rating_given' : rate,
                    'title' : title, ##title is likely to produce borked results. this one is just an isbn. soo..yeah
                    'user': soup.find_all(class_ = re.compile('user'))[0].attrs['href'][11:],
                    'language' : language
                          }

    save_to_mongo(formatted_dct, db, coll)

if __name__ == "__main__":
    option = webdriver.FirefoxOptions()
    option.add_argument('-headless')
    print("Hello, I'm just getting everything together")
    driver =  webdriver.Firefox(options=option)
    actions = ActionChains(driver)
    
    nlp = spacy.load("en")#get information and make pipe for the language detection
    nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)

    


    first_page = True
    samples = list(np.arange(1,7000000)) # the bookreads books are...bad. 
    print('checking on the samples!')

    current_index = get_last_index()
    print('everything seems to be in order.')
    print(current_index)

    for book_id in samples[int(current_index):-1]:
        print("**stretches**")
        current_index+=1
    #         current_index = samples.pop()
        
        get_next_page(book_id)
        time.sleep(1)

        if (str(book_id)in driver.current_url) != True:
                
                print(book_id)
                print("Uhhh....I'm a little confused, but somehow I ended up at {}".format(driver.current_url))
                continue
    #         print('loading '+book_review_url)

        if first_page == True:
                click_in_margin()
                first_page = False

        #print('scrolling down')
        #scroll_to_bottom(1.5)  # let the website load for 1.5 secs...ugh
        print('scooping reveiws')
        review_lst = each_page()
        for items in review_lst:
            cleaned =clean_one(items, nlp)
        #save_to_mongo(review_lst)
        #add doc to mongodb # clean_one() now inserts to mongo
        log_current_sample()
        print('book {} done, now sleeping'.format(book_id))
        time.sleep(1) #sleep now exists in the go to the next page step. . 
    #end loop

driver.close()

