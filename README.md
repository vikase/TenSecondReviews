#TenSecondReviews

A quick summarization of product reviews.
=============



#### Inspiration
A New Jersey based company called C&A is doing 9-figures in sales by 1) tracking best-selling amazon products, 2) identifying customer requests for new features, 3) manufacturing these slightly modified products, and then 4) selling them through online channels.  

In order to do 1) and 2), C&A has a team of over 20+ people reading Amazon reviews.

I started with a single question: Given a product is it possible to use natural language processing to identify the new features or fixes that customers are requesting automatically?   

Investigating further I noticed that these "suggested improvements" were often related to a particular attribute (or feature or aspect) of the product.  For example, for a certain micro mobile speaker set, there were many requests for a waterproof remote control and for longer battery life. 

Was it possible to extract the attribute (remote control, battery life) and also discover the way consumers felt about these particular attributes?  

And if it was possible, could I then quickly compare that product's attributes with other products in it's category?



#### Data
Jure Leskovec and Andrej Krevl host an Amazon dataset that spans a period of 18 years up to March 2013 as part of the Stanford Large Dataset Collection.  It can be found here: https://snap.stanford.edu/data/web-Amazon.html

For the purposes of this project, I limited myself to electronic product reviews.  

Each category (cameras, laptops, phones, etc.) has a collection of json files, and each json represents a particular product; it contains all the reviews associated with that product, and other metadata related to the product.

Looking at the camera category specifically, there were initially 3007 unique products.  This was refined down to 1108 products which had more than 100 reviews each for a total of 322,035 camera reviews analyzed (an average of 300 reviews per product.

#### Overview
The main steps were organizing the data, extracting the relevant features, and then creating sentiment scores for each of the features per product.

#### Organizing the Data
I transformed the data into a pandas dataframe (one review per row), which I then filtered to preserve only products which contained at least 100 reviews.  This was not strictly necessary (as will be seen in the "creating sentiment scores" section), however it has the benefit of increasing the probability that every camera has at least one aspect mentioned. 

#### Extracting the Features
There are multiple methodologies to extracting features/aspects in NLP literature.  Some of these involve finding highly frequent phrases across the reviews and filtering by rules such as "occurs right after sentiment word."  An example of this for a Mexican restaurant's reviews might be "(great) fish tacos". 

Another method is to hand label sentences or phrases with the features you are interested in.  Again going back to the restaraunt example, this would entail hand labeling certain phrases with tags like ('food', 'decor', 'service', 'value).  The next step would be to train a classifier to assign aspects to a sentence. 

#### Collocations 
The method adopted either here involves finding collocations.  A collocation is an expression consisting of two or more words that correspond to some conventional way of saying things.  Another way of saying this is collocations are common expressions (often idioms) found within a specific language context.  Some examples from the corpus of everyday speech might include ('regular exercise', 'utterly stupid', 'ran out of money', 'whispered softly').  Collocations are characterized by limited compositionally, which means the meaning of the expression can only partially be predicated from the meaning of its parts. ie. 'strong tea' does not mean a tea having great physical strength, but rather a rich tea.  There is an element of added meaning in a collocation.  

There are several approaches to approaches to finding collocations in a corpus: selection of collocations by frequency and  selection based on mean and variance of the distance between focal word and collocating word among others.

#### Extracting the Features (Cont.)
Here we calculated collocations using the Jaccard Index.  The corpus of reviews was broken up into 'key bigrams'. The frequency of the key bigram frequency was counted and then divided by the sum of frequencies with which any bigram contained a term in the bigram of the 'key bigram'.  

An illustrative example.  "The dance revolution must continue.  You can dance if you want to.  But dance revolution is the wave of the future."  Here "dance revolution" is one of many 'key bigrams' extracted from this corpus containing three sentences.  'dance revolution' has a frequency of 2.  The sum of frequencies of the bigrams in this corpus that contain a word from this 'key bigram' is 8 (it includes for example, 'the dance', 'dance revolution', and 'revolution must', but not 'must continue' which contains neither 'dance' or 'revolution'). The jaccard index for this 'key bigram' would then be 1/4.  

Other scoring methods to find collocations include Dice's coefficient and the likelihood ratio.  See Foundations of Statistical Natural Language Processing by Manning and Schuetze for more.

NLTK has an implementation of collocations which was used for this project.

####Collocations in this Amazon camera dataset

The features extracted with this method included [low light; memory card; picture quality; battery life; image quality; highly recommend; wide angle; shutter speed; takes great; optical zoom; great pictures; lcd screen; image stabilization; digital camera; touch screen; much better; would recommend; year old].  

Not all of these features that we would like to actually rank our products upon.  Certainly not on "highly recommend" or "much better".  Initially the process to eliminate these, for the purposes of this proof of concept, was manual.

#### Creating Sentiment Scores For Each Feature per Product

Having collected the relevant features for a particular product.  The next step was to assign a score for each of the features per product.  For this we constructed a scoring set based on Bing Liu's Opinion Lexicon 
(https://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html).  This is a lexicon that consists of about 6800 positive and negative words that have been compiled over many years.

We then collected every sentence fragment that contained a feature and scored the feature +1 for positive modifiers in that fragment, and -1 for negative modifiers present in that fragment.  Each phrase could only increment the sentiment score by +1, even if there were multiple positive modifiers in the phrase.  This was done to prevent overly enthusiastic reviewers from skewing the results.

This is admittedly a brute force technique.  There will be instances where within the sentence fragment, the aspect will be mentioned and the sentiment word that is in the same phrase is not modifying the aspect we are measuring but some other aspect.  However, based on how we are creating sentence fragments, this is an inexpensive method to get approximate results.

Moreover, we adjusted the score to account for products which simply had more reviews (and therefore if there was a bias found in reviewers across reviewers ie. reviewers tend to be leave positive reviews when they leave reviews) 

#### Conclusions and Results




#### Necessary Python Packages ####
1. cPickle
2. Flask - just for webapp
3. Matplotlib
4. Numpy
5. Pandas
6. Plotly
7. Scikit-Learn
8. Scipy
9. Werkzeug - just for webapp 
