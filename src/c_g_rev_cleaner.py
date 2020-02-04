from pymongo import MongoClient
import pprint
import json
import bs4
from bs4 import BeautifulSoup
import re
import numpy as np

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
    db = client[db]
    collection = db[collection]
    
    collection.insert_many(add_this) 
    #add doc to mongodb
    client.close()

    if __name__ == "__main__":
    
    client = MongoClient('localhost', 27017)
    db=client['reviews']
    coll=db['book_reviews']
    documents = [x for x in db['book_reviews'].find()]
    
    ##for loop going throuhg all documents
    all_revs = []
    for i in documents:
        breakpoint = documents.index(i) ##will show me where this thing breaks

        soup = BeautifulSoup(i['reviews'], 'html.parser')
        readable = soup.find_all(class_ = "readable")
        
        
        nlp_words = get_text(readable)
        if nlp_words == -1:
            continue
            
        

        try: #some people are leaving reviews without giving the books any stars. interesting. 
            rate_string = soup.find_all(class_ = re.compile('staticStars notranslate'))[0].attrs['title']
            rate = str_to_rate(rate_string.split())
        except IndexError:
            rate = -1
        
        try: #catching the documents with nothing in them. 
            title = soup.find_all(class_ = re.compile('lightGreyText'))[0].attrs['title'], ##title is likely to produce borked results. this one is just an isbn. soo..yeah
        except IndexError:
            title = -1
            
            
        user = soup.find_all(class_ = re.compile('user'))[0].attrs['href'][11:]
        
        sub_rev = [rate, user, title, nlp_words]
        all_revs.append(sub_rev) 
        #progress_bar = documents.index(i)
        #update_progress(documents.index(i) / len(documents))
#         if progress_bar % 100 ==0:
#             print(progress_bar)
        
    client.close()            
    np.save("data/cleaned", all_revs) ## might need to do a mongo thing
    
    # # mongo thing GOES INSIDE THE LOOP
#         formatted_dct = {'book_id' : i['book_id']
#                          'nlp_words' : get_text(readable),
#                          'rating_given' : rate,
#                          'title' : title, ##title is likely to produce borked results. this one is just an isbn. soo..yeah
#                          'user': soup.find_all(class_ = re.compile('user'))[0].attrs['href'][11:]
#                         }



#update_progress(1)