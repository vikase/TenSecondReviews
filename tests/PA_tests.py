def create_list_of_reviews_for_product(Id):
    '''
    Function to create list of reviews available for a single product
    '''
    df_product = df[df.ProductID == Id]
    product1_reviews =  df_product.Review.str.lower()
    review_list = product1_reviews.tolist()   
    return review_list

def create_top10_keywordlist(keywords_collocation_format):
	'''
    Function to check top keywords
    '''
    keyword_top10 = keywords_collocation_format.split(";")
    top10 = []
    for word in keyword_top10:
        top10.append(word.strip())
    return top10


