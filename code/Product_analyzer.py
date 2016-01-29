
# coding: utf-8

# In[ ]:

#https://www.appannie.com/
#Sf based
#Recently raised 50mm + 
#Provides intelligence about apps; including analysis of reviews

#Document why you are doing things not what you are doing.


# In[ ]:

#Each model will have a dictionary with 10 keywords as keys and 
#with a list of tuples as values, where each tuple contains a sentiment word
#describing that feature, and a polarity score associated with that word.

#lemmatize?

#For model_reviews in product_line_reviews:
    #For review in model_reviews:
        #For feature in keyword_top10:
            #search review (maybe using concordance or else using regex) \n
            #to find sentences where feature is mentioned.
            
            #NLP portion
                #Extract the sentiment word that describes the feature and assign polarity.
                #(returns sentiment word, polarity) and appends that pair to 
                # the value of a dictionary 
                #where the key = feature and value = list of pairs.
                
                #Ten dictionaries for each feature.  
                #Create a wordcloud out of the values, where size of word
                #is based on number of occurences, and cloud is split into two halves
                #where posive sentiment words are on one side and negative on other
            
# One possible way to improve this algorithm 
# workflow would be to identify the keywords and then bring the sentences 
# where keyword is mentioned.  
# Then Determine patterns in syntactic structure that would help 
# pull parse those sentences properly for the relevant sentiment word.
            
#A test review:
#"The camera does not handle low light conditions well."


# In[145]:

import pandas as pd

import spacy
from spacy.en import English

from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from textblob import Word

import nltk
from nltk import FreqDist

from collections import namedtuple


# In[15]:

def main():
    nlp = English()
    positive, negative = create_keyword_sentences()
    df, df_grouby100, camera_IDs = product_dataframe("./camera_reviews_test.csv")




# In[237]:

def create_sentiment_lexicon():
    '''
    Getting Opinion Lexicon from Bing Liu
    Positive and Negative word lists

    positive and negative are both lists.  positive contains the word "good".

    '''

    fname = "./sentiment/opinion-lexicon-English/positive-words.txt"
    with open(fname) as f:
        positive = f.read().splitlines()
        positive = [s for s in positive if not s.startswith(";")]
    garbage = positive.pop(0)

    fname = "./sentiment/opinion-lexicon-English/negative-words.txt"
    with open(fname) as f:
        negative = f.read().splitlines()
        negative = [s for s in negative if not s.startswith(";")]
    garbage = negative.pop(0)

    return positive, negative



def product_dataframe(file_name):
    '''
    Starting with 3007 unique products
    # print len(df.ProductID.unique())
    # 3007 unique products

    Create new dataframe with 1108 products which have more than 100 reviews each
    # print len(df_groupby_100.index.unique())
    # There are 1108 products with greater than 100 reviews

    List of ProductID>100reviews stored in camera_IDs

    #print camera_IDs
    #>['B00004R8V6' 'B00004R8VC' 'B00004TS16' ..., 'B00HFUXKJQ' 'B00HFUXLZE' 'B00I6TC6XG']

    '''

    df = pd.read_csv(file_name)
    df_groupby = df.groupby('ProductID').count()
    df_groupby_100 = df_groupby[df_groupby['Name']>100]
    camera_IDs =  df_groupby_100.index.values
    return df, df_grouby100, camera_IDs



def create_list_of_reviews_for_product(Id):
    '''
    Function to create list of reviews available for a single product
    '''
    df_product = df[df.ProductID == Id]
    product1_reviews =  df_product.Review.str.lower()
    review_list = product1_reviews.tolist()   
    return review_list


def create_dictionary_products_reviews(camera_IDs):
    '''
    Function to create dictionary with products as keys and values as list of reviews
    '''
    review_dict = {}
    for ID in camera_IDs:
        review_dict[ID] = create_list_of_reviews_for_product(ID)
    return review_dict

    review_dict = create_dictionary_products_reviews(camera_IDs)


'''
Collocations already provides a good high level summary of the discussion 
occuring on this product.
'''

from nltk.text import Text  

def create_review_corpus_from_list(review_list):
    review_corpus = "".join(review for review in review_list)
    return review_corpus

def create_nltk_text_object(review_corpus):
    tokens = nltk.word_tokenize(review_corpus)
    text = nltk.Text(tokens)
    review_text_obj = Text(text)
    return review_text_obj

def nltk_collocations(review_text_object):
    review_text_object.collocations()
    
def nltk_concordance(review_text_object, keyword):
    review_text_object.concordance(keyword)



'''
all_reviews aggregrates review_list.values into one list that contains all the reviews.
This contains 322035 reviews for the subset-ed camera dataset.

#print len(all_reviews)
#323045 = num reviews in all_reviews
'''
all_reviews = []
for product in review_dict.keys():
    all_reviews += review_dict[product]



'''
See The features brought out looking at all the products
'''
#This takes a long time to run (10 minutes or so) - Needs to be saved

all_review_corpus = create_review_corpus_from_list(all_reviews)
all_review_text_object = create_nltk_text_object(all_review_corpus)
nltk_collocations(all_review_text_object)


# In[148]:

#This was saved manually - but should be stored or created based on the review corpus being studied

keywords_collocation_format = "low light; memory card; picture quality; battery life; image quality; highly recommend; wide angle; shutter speed; takes great; optical zoom; great pictures; LCD screen; image stabilization; digital camera; touch screen; much better; would recommend; year old; Digital Camera; view finder"

#keyword_top10 = top 10 keywords from all reviews
def create_top10_keywordlist(keywords_collocation_format):
    keyword_top10 = keywords_collocation_format.split(";")
    top10 = []
    for word in keyword_top10:
        top10.append(word.strip())
    return top10

top10_keyword_list = create_top10_keywordlist(keywords_collocation_format)
print top10_keyword_list


# In[328]:

'''
Functions to create keyword_sentence_list to perform sentiment analysis upon.
Takes a string and returns a list.

Needs to be modified (or anther function must be written) to create multiple product
keyword_sentence_lists.

Create keyword_sentence_list_dict for multiple products

#This serves as an improvement over nltk_concordance
review_searchTerm = "finder"
nltk_concordance(review_text_object, review_searchTerm)
'''

import re

keyword = "battery life"

def first_closing_punctuation_after_first_keyword(text, index):
    period  = text.find(".",index)
    exclamation = text.find("!", index)
    question = text.find("?",index)  
    colon = text.find(":", index)
    semicolon = text.find(";",index)
    comma = text.find(",",index)  
   
    b_period  = text.rfind(".", 0, index)
    b_exclamation = text.rfind("!", 0 ,index)
    b_question = text.rfind("?", 0 ,index)
    b_colon = text.rfind(":", 0, index)
    b_semicolon = text.rfind(";",0, index)  
    b_comma  = text.rfind(",", 0, index)

    return max(b_period, b_exclamation, b_question, b_colon, b_semicolon, b_comma),             min(period, exclamation, question, colon, semicolon, comma)

def create_keyword_sentences(text, keyword):
    index_position_of_keyword = [m.start() for m in re.finditer(keyword, text)]

    keyword_sentences = []
    for index in index_position_of_keyword:
        punc_positions = first_closing_punctuation_after_first_keyword(text, index)
        if len(text[punc_positions[0]+1:punc_positions[1]+1])>2:
            keyword_sentences.append(text[punc_positions[0]+1:punc_positions[1]+1])
    return keyword_sentences

def create_keyword_sentence_list_dict(product_ID_list, review_dict, keyword):
    keyword_sentence_dict = {}
    for product in product_ID_list:
        keyword_sentence_dict[product] = create_keyword_sentences(create_review_corpus_from_list(review_dict[product]), keyword)
    return keyword_sentence_dict


# In[274]:

keyword_sentence_list = create_keyword_sentences(one_review_corpus, keyword)
battery_life_sentence_dict = create_keyword_sentence_list_dict(camera_IDs, review_dict,  "battery life")


# In[331]:

'''
keyword_sentiment_across_products(IDs, keyword):
#Calculate sentiment scores for keyword across all products
#Also provides the highest and lowest rated products for that keyword

sentiment_scores_per_sentence excludes products where keyword is referenced less than 5 times \
among all it's reviews.
'''

def keyword_sentiment_across_products(IDs, review_dict, keyword):
    keyword_product_dict = create_keyword_sentence_list_dict(IDs, review_dict, keyword)
    sentiment_keyword_dict = {}
    max_score_ratio = (0, 0)
    min_score_ratio = (0, 0)
    for ID in IDs:
        sentiment_keyword_dict[(ID, keyword)] = \
        sentiment_scores_per_sentence(keyword_product_dict[ID])     
        
        if sentiment_scores_per_sentence(keyword_product_dict[ID])[0]>max_score_ratio[1]:
            max_score_ratio = (ID, sentiment_scores_per_sentence(keyword_product_dict[ID])[0])
        if sentiment_scores_per_sentence(keyword_product_dict[ID])[0]<min_score_ratio[1]:
            min_score_ratio = (ID, sentiment_scores_per_sentence(keyword_product_dict[ID])[0])                          
    return (sentiment_keyword_dict, max_score_ratio, min_score_ratio)

def sentiment_scores_per_sentence(text, audit = False):
    total_score = 0
    num_sentences = len(text)

    if num_sentences < 5:
        return (0, 0, 0)
    
    for sentence in text:
        positive_score = 0
        negative_score = 0
        wordSet = set(sentence.split(" "))
        for word in positive:
            if word in wordSet:
                positive_score += 1
        for word in negative:
            if word in wordSet:
                negative_score +=1
        if audit == True:
            print sentence
            print (positive_score, negative_score)
        total_score += positive_score - negative_score
    
    score_ratio = float(total_score)/num_sentences

    return (score_ratio, total_score, num_sentences)


# In[333]:

ID_keyword_dict = keyword_sentiment_across_products(camera_IDs, review_dict, keyword)
print ID_keyword_dict[1], ID_keyword_dict[2]

# sentiment_scores_per_sentence(product2_batterylife_list, audit = True)

'''
# Results for keyword = battery life
#('B00B7N9A5A', 3.5) ('B001DEYVXO', -1.0)
#Results after excluding less than 5 occurences of keyword:
#('B000M4J2OO', 3.3333333333333335) ('B003VTZE0I', -0.4444444444444444)
# Results after lowercasing
('B0032JRRWU', 2.0) ('B004HO59XS', -0.5)

'''


# In[339]:

# print create_keyword_sentence_list_dict(["B000M4J2OO"], keyword)
productID = "B000H91K7Q"
sentiment_scores_per_sentence(create_keyword_sentence_list_dict([productID], review_dict, keyword)[productID], audit = True)

