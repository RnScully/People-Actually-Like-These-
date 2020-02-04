# Predictotron

### Namechange pending. 
This is a product review project focusing on book reviews from goodreads. It includes a script for scraping the goodreads website, and another for cleaning the data from json files into cleanly schemaed data.

I hope to provide a model which predicts what average star rating a reveiw is likely to peg a book at, tell you how skewed from a "uniform" rating that would be. 


### Tech Stack
- python, numpy, re, BeautifulSoup
- Selenium
- spacy_langdetect
- VADER-Sentiment-Analysis


### Further Work:
- take further advantage of Vader's ! emphasis technology by adding functionality to remove_text_inside_brackets that replaces '<\b>' (the close-bold) with '!'

- Build out foreign language sentiment analysis, check if culture matters for the seriousness of your average user-made book rating
