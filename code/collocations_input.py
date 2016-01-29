
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
import subprocess

# nlp = English()

import sys
from cStringIO import StringIO

import pickle

'''
Collocations already provides a good high level summary of the discussion 
occuring on this product.
'''

def create_nltk_object():
	product1 = "B00004R8V6"

	product1_review_list = review_dict[product1]
	one_review_corpus = create_review_corpus_from_list(product1_review_list)
	review_text_object = create_nltk_text_object(one_review_corpus)

	with open('test.pickle', 'wb') as handle:
  		pickle.dump(nltk_object, handle)


def feature_extractor(nltk_object):
	'''
	'''
	# setup the environment
	backup = sys.stdout
	# ####
	sys.stdout = StringIO()     # capture output
	nltk_collocations(review_text_object)

	features_string = sys.stdout.getvalue() # release output

	sys.stdout.close()  # close the stream 
	sys.stdout = backup # restore original stdout

    feature_list = []
    for feature in features_string.split(";"):
        feature_list.append(feature.strip())
    return feature_list


def create_corpus(review_list):
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


def filter_products_make_dict(file_path, min_reviews_per_product = 100):
	'''Creates dictionary of reviews for products with at least 100 reviews
		Args: file_path : a csv file that was created from json files /
						  through JSON_to_Pd
		Returns:
			df (dataframe): dataframe containing all products in category /
							with each row containing a review
			IDs (list) : list of product IDs that will be examined
			review_dict (dict) : dictionary with IDs as keys and a list of reviews as values
			all_reviews (list) : every review for the product category, collected in a list
								This contains 322035 reviews for the subset-ed camera dataset.

	'''
	df = pd.read_csv(file_path)
	df_groupby = df.groupby('ProductID').count()
	df_groupby_100 = df_groupby[df_groupby['Name']>min_reviews_per_product]
	IDs =  df_groupby_100.index.values

	review_dict = {}
	all_reviews = []

    for ID in IDs:
    	df_product = df[df.ProductID == ID]
    	ID_review_series = df_product.Review.str.lower()
    	ID_review_list = ID_review_series.tolist()  
        review_dict[ID] = ID_review_list
        all_review_list += ID_review_list

	# all_review_corpus = create_corpus(all_review_list)
	# all_review_text_object = create_nltk_text_object(all_review_corpus)
	# c = all_review_text_object.collocations()

	with open('df.pickle', 'wb') as handle:
  		pickle.dump(df, handle)

  	with open('IDs.pickle', 'wb') as handle:
  		pickle.dump(IDs, handle)

  	with open('review_dict.pickle', 'wb') as handle:
  		pickle.dump(review_dict, handle)

  	with open('all_reviews.pickle', 'wb') as handle:
  		pickle.dump(all_reviews, handle)

  	with open('all_reviews.pickle', 'wb') as handle:
  		pickle.dump(all_reviews, handle)


if __name__ == '__main__':
	#product file path
	file_name = "./camera_reviews_test.csv"
	#dataframe, IDs, and reviews stored in dictionary
	df, IDs, review_dict, all_review_corpus = filter_products_make_dict(file_name)

	#Create Pickle files of the products you will be examining


	#calculate collocations for corpus of reviews






    


