
import pandas as pd
import json
import matplotlib.pyplot as plt
import os, sys, glob

def make_csv(json_file_location):
	'''
	Loop through each JSON file in project>AmazonReviews>cameras

	The first step is to extract the attributes themselves.
	This can be done across all cameras.  

	Becaause there are probably subgroups of cameras, 
	Can also try to group these cameras into categories first
	And then try to figure out how the discussion is progressing.

	Unsupervised clustering of reviews 
	'''

	listing = glob.glob()

	df = pd.DataFrame(columns = ['Author', 'Content', 'Date', 'Overall', 'ReviewID', 'Title',
	       'Review', 'Price', 'ProductID', 'Features', 'ImgURL', 'Name'])

	for product in listing:
		with open(product) as json_data:
			d = json.load(json_data)
			json_data.close()
		

		if len(d['Reviews'])>20:

			df_review = pd.DataFrame(d['Reviews'])

			df_review['Title'] = df_review['Title'].map(lambda x: x if x[-1] in ['.','!'] else x + '.')

			temp = df_review.Title + df_review.Content

			if temp.isnull().values.any():
				continue

			df_review['Review'] = df_review.Title + df_review.Content

			df_review = df_review.drop(['Title', 'Content'], axis = 1)

			columns = ['Name', 'Author', 'Features']

			for column in columns:
				df_review[column] = df_review[column].map(lambda x: x.encode("ascii", "ignore") if x else None) 

			df_review['Review'] = df_review['Review'].map(lambda x: x.encode("ascii", "ignore"))

			for key in ['Price', 'ProductID', 'Features', 'ImgURL', 'Name']:
				df_review[key] = d['ProductInfo'][key]

			df = df.append(df_review)

	df.to_csv("camera_reviews_test2.csv")











