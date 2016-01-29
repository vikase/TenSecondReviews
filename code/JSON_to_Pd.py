'''
Bringing reviews back for just one camera
'''

import pandas as pd
import json
import matplotlib.pyplot as plt



'''

Loop through each JSON file in project>AmazonReviews>cameras

The first step is to extract the attributes themselves.
This can be done across all cameras.  

Becaause there are probably subgroups of cameras, 
Can also try to group these cameras into categories first
And then try to figure out how the discussion is progressing.

Unsupervised clustering of reviews 
'''

import os, sys, glob

# path = "AmazonReviews/cameras/"
# dirs = os.listdir(path)

listing = glob.glob('AmazonReviews/cameras/*.json')
print len(listing)
print listing[0]


df = pd.DataFrame(columns = ['Author', 'Content', 'Date', 'Overall', 'ReviewID', 'Title',
       'Review', 'Price', 'ProductID', 'Features', 'ImgURL', 'Name'])

for product in listing:
	# print product 

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

print df.shape
print len(df.ProductID.unique())
df.to_csv("camera_reviews1_test2.csv")

#There is some error - there are 3075 unique productID's but only 2 are being saved to this CSV.
#UnicodeEncodeError: 'ascii' codec can't encode character u'\xa0' in position 1580: ordinal not in range(128)











#####################################################

#UNUSED

#####################################################


#Test Individual products
def review_tester():
	file_name = "AmazonReviews/cameras/1080100008.json"

	with open(file_name) as json_data:
	    d = json.load(json_data)
	    json_data.close()

	print d


	print "reviews:"
	print d['Reviews']

	df = pd.DataFrame(d['Reviews'])

	print "productsInfo"

	print d['ProductInfo']
	df = pd.DataFrame(d['ProductInfo'], index=[0])

	df = pd.DataFrame(columns = ['Author', 'Content', 'Date', 'Overall', 'ReviewID', 'Title',
	       'Review'])

	df_review = pd.DataFrame(d['Reviews'])

	df_review['Title'] = df_review['Title'].map(lambda x: x if x[-1] in ['.','!'] else x + '.')

	df_review['Review'] = df_review.Title + df_review.Content

	for key in ['Price', 'ProductID', 'Features', 'ImgURL', 'Name']:
		df_review[key] = d['ProductInfo'][key]

	df.append(df_review)

	print df.head()

# review_tester()

	# df_productinfo = pd.DataFrame(d['ProductInfo'], index = [0])


# for key, val in d['ProductInfo'].iteritems():
# 	df_review[key] = val
# df_review = df_review[['review', '']]

# dfs = []
# for jsonfile in files:
# 	dfs.append(df_review)

#Add this product info row as new columns for every column in review

# print df_review.ix[:, 8]



############################


#save to csv




# print df

# df = pd.DataFrame(columns = ['Author', 'Content', 'Date', 'Overall', 'ReviewID', 'Title',
#        'Review'])
# print df.columns

# for file_name in listing:
# 	with open(file_name) as json_data:
# 	    d = json.load(json_data)
# 	    json_data.close()

# 	if d['ProductInfo']['Name'] is None:
# 		pass
# 	# 	print d['ProductInfo']['Features']
# 	# print len(d['Reviews'])
# 	else:
# 		df = pd.DataFrame(d['Reviews'])

# 		df['Title'] = df['Title'].map(lambda x: x if x[-1] in ['.','!'] else x + '.')

# 		df['Review'] = df.Title + df.Content

# print df.Title



'''
Build N-grams from the sum of the reviews across cameras?
See what TF-IDF looks like for that corpus.  

'''





'''
Loop through each JSON file in project>AmazonReviews>cameras
if len d['Reviews]>20 
and if d['ProductInfo']['Name'] != "NULL" & d['ProductInfo']['Price'] != "NULL"

create df with Reviews and Features


'''

'''


Multiple Reviews per ProductID

Group by ProductID

Filter out instances where Price and Name do not exist

See Distribution of Count of ProductID

List of ProductID where Count of ProductID > 20

newDF that includes only those ProductID's  where Count of ProductID > 20
'''







