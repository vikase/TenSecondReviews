#TenSecondReviews

A quick summarization of product reviews.

=============



#### Inspiration
A New Jersey based company called C&A is doing 9-figures in sales by 1) tracking best-selling amazon products, 2) identifying customer requests for new features, 3) manufacturing these slightly modified products, and then 4) selling them through online channels.  

In order to do 1) and 2), C&A has a team of over 20+ people reading Amazon reviews.

I started with a single question: Given a product is it possible to use natural language processing to identify the new features or fixes that customers are requesting automatically?   

Investigating further I noticed that these "suggested improvements" were often related to a particular attribute (or feature or aspect) of the product.  For example, for a certain micro mobile speaker set, there were many requests for a waterproof remote control and for longer battery life. 

Was it possible to extract the attribute (remote control, battery life) and also discover the way consumers felt about these particular attributes?  

And if it was possible, could I then quickly compare that product's attributes with other product's in it's category?


#### Data
Jure Leskovec and Andrej Krevl host an Amazon dataset that spans a period of 18 years up to March 2013 as part of the Stanford Large Dataset Collection.  It can be found here: https://snap.stanford.edu/data/web-Amazon.html

For the purposes of this project, I limited myself to electronic product reviews.  

Each category (Cameras, laptops, phones, etc.) has a collection of json files that each represent a particular product, all the reviews associated with that product, and other metadata related to the product.

#### Repetition Detection
Once the pushup duration window is calculated, Workout Buddy uses peak detection algorithms, on the unfiltered pitch data, to pick out the press-down and push-up times for each repetition in the set. The maximum press-down amplitude and the repetition duration are extracted for classifying the pushup form. In addition, the entire pitch and y-acceleration repetition time series are used during the classification process (See process_data.py and detect_peaks.py for more details).

#### Exercise Classification and Rating
Workout Buddy uses an ensemble of classifiers to provide detailed ratings of your latest workout. It uses Random Forest and Support Vector Machine classifiers to model the amplitude and repetition duration features. Dynamic Time Warping, a method of calculating the distance between time series, is used in combination with K-Nearest Neighbors to classify the repetition time series. Each of the models provides a probability that the pushup repetition is either 'ok' or 'good'. The ensemble of models are combined, with equal weights. Workout Buddy uses the binary classification, along with the probabilities, to provide detailed ratings of your set of pushup repetitions (see classify.py and dtw.py for more details).

#### Interactive Visualizations
Workout Buddy provides several interactive visualizations of your latest workout, and your workout history, on the webapp dashboard. Plotly is used to make the interactive plots (see plotly_graphs.py for more details). There are two visualizations of your latest set of repetitions. The first visualization plots the pitch time series for each repetition, so you can see the variability in your set. An optimal pushup repetition is also plotted, so you can see how close you are to performing an expert pushup. The next visualization is a bar chart of your latest set of repetitions, plotted sequentially. The size of the bar corresponds to the rating of the repetition, with 0% being poor and 100% being excellent form. The rating is the probability of your repetition being 'good' from the ensemble classification model. The bar is colored according to the binary classification of 'ok' (colored red) or 'good' (colored green). The last visualization is a stacked bar chart of your past 30 days of activity, showing the number of 'ok' and 'good' repetitions.

==============
#### Implementation Details ####
The code, and the data to train your own classifiers, is provided and can be run with the script training_pipeline.py. You can also use the provided models to classify your own data with the script user_prediction_pipeline.py (for data with user info) or anon_prediction_pipeline (for anonymous sensor data). Run setup.py first to set up the necessary directory structure.

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
