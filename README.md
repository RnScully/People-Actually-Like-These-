# Predictotron

### Namechange pending. 
This is a product review project focusing on book reviews from goodreads. It includes a script for scraping the goodreads website, and another for cleaning the data from json files into cleanly schemaed data.

I hope to provide a model which predicts what average star rating a reveiw is likely to peg a book at, tell you how skewed from a "uniform" rating that would be. 

### Insights and Stats
40627 reviews pulled in initial run, 
97.6% englihs, 2.4% non-english. 

##Process
Scraped data from Goodreads, pulled data from Amazon's review's S3
Removed all non-english reviews. 

removed all negation terms from stopwords to give the n-grams the ability to encapsulate negation. 

Tokenized all reveiws as 2-grams to capture word order and negation terms. 

Fit random forest to the data

### Tech Stack
- python, numpy, re,
- Selenium, BeautifulSoup
- nltk, spacy_langdetect, 


### Further Work:
- take further advantage of Vader's ! emphasis technology by adding functionality to remove_text_inside_brackets that replaces '<\b>' (the close-bold) with '!'

- Build out foreign language sentiment analysis, check if culture matters for the seriousness of your average user-made book rating

- take advantage of the ISBNS to sort by genre type and make calls to google or amazon or goodreads api to get more information about books

