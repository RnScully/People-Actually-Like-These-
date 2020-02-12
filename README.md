# People Actually Like These!

This is a product review project focusing on book reviews from goodreads. It includes a script for scraping the goodreads website, and another for cleaning the data from json files into cleanly schemaed data.

The model is a random forest trained on book review data to predict numerical rating good/bad (good being 4 and 5, bad being 3 and below), a statistc based on the distribution of ratings in my corpus, shown below. 

<img src="img/ratings_hist.png">
With 39644 reviews in my corpus

### Insights and Stats
40627 reviews 
97.6% english, 2.4% non-english. 


## Process
Scraped data from Goodreads, pulled data from Amazon's review's S3
Removed all non-english reviews. 

removed all negation terms from stopwords to give the n-grams the ability to encapsulate negation. 

Tokenized all reveiws as 2-grams to capture word order and negation terms. 

vectorized tokens using TFiDF to produce numeric arrays that the forest could use, selected 5000 features as near-optimal. 

Fit random forest to the data, tune, iternate. 







### Tech Stack
- python, numpy, re,
- Selenium, BeautifulSoup
- nltk, spacy_langdetect
- SKlearn TFIDFVectorizor, RandomForestClassifier


### Further Work:
- take further advantage of Vader's ! emphasis technology by adding functionality to remove_text_inside_brackets that replaces '<\b>' (the close-bold) with '!'

- Build out foreign language sentiment analysis, check if culture matters for the seriousness of your average user-made book rating

- take advantage of the ISBNS to sort by genre type and make calls to google or amazon or goodreads api to get more information about books

