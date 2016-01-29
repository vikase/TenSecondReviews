import pandas as pd

import spacy
from spacy.en import English

from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from textblob import Word

import nltk
from nltk import FreqDist
from nltk.text import Text  

from collections import namedtuple

import re

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



def create_dictionary_products_reviews(camera_IDs):
    '''
    Function to create dictionary with products as keys and values as list of reviews
    '''
    review_dict = {}
    for ID in camera_IDs:
        review_dict[ID] = create_list_of_reviews_for_product(ID)
    return review_dict

    review_dict = create_dictionary_products_reviews(camera_IDs)


def create_list_reviews(review_dict):
    '''
    all_reviews aggregrates review_list.values into one list that contains all the reviews.
    This contains 322035 reviews for the subset-ed camera dataset.

    #print len(all_reviews)
    #323045 = num reviews in all_reviews
    '''

    all_reviews = []
    for product in review_dict.keys():
        all_reviews += review_dict[product]
    return all_reviews


def create_collocations(all_reviews):
    '''
    See The features brought out looking at all the products
    '''
    #This takes a long time to run (10 minutes or so) - Needs to be saved
    #as NLTK collocations is outputted to terminal

    all_review_corpus = create_review_corpus_from_list(all_reviews)
    all_review_text_object = create_nltk_text_object(all_review_corpus)
    nltk_collocations(all_review_text_object)
    return nltk_collocations

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

    return max(b_period, b_exclamation, b_question, b_colon, b_semicolon, b_comma),   \
              min(period, exclamation, question, colon, semicolon, comma)

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


def keyword_sentiment_across_products(IDs, review_dict, keyword):

    '''
    keyword_sentiment_across_products(IDs, keyword):
    #Calculate sentiment scores for keyword across all products
    #Also provides the highest and lowest rated products for that keyword

    sentiment_scores_per_sentence excludes products where keyword is referenced less than 5 times \
    among all it's reviews.
    '''
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
    '''
    Creates sentiments scores for each attribute in the product review

    '''
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

def main():
    json_file_location =  'AmazonReviews/cameras/*.json'
    make_csv(json_file_location)
    product_location = "./camera_reviews_test.csv"
    
    nlp = English()
    positive_words, negative_words = create_keyword_sentences()
    df, df_grouby100, IDs = product_dataframe(product_location)
    review_dict = create_dictionary_products_reviews(IDs)
    all_reviews = create_list_reviews(review_dict)
    collocations = create_collocations(all_reviews)
    keyword_sentence_list = create_keyword_sentences(all_reviews, collocations)
    sentiment_score_per_keywords = sentiment_scores_per_sentence(keyword_sentence_list, audit = False):


