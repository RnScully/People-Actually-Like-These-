## Factor Day Trading
Online brokerages have fought a race to the bottom on trade pricing, and you can now buy and sell stocks with 0 transaction price. This means you can daily make trades on a variety of predictions, and possibly do well, provided you have made the right predictions.

I expect to need to employ webscraping technologies, regressions, and likely random forests and boosted trees for the predictions. 

This project will produce a report of top suggestions for daily stock buys, and as a further goal, an automation app that will spend X money on a stock buying website employint its suggestions


### Data Sources
https://www.nyse.com/listings_directory/stock
NYSE stock index, and anything else I can reasonably include

## Are books actually good?

Book ratings are actually absolutely wrong. I mean, shoot, 3 out of 5 ratings are 5 star ratings. That's borked. 

We can do better! Take book reviews from Goodreads, Amazon, and Possibly Kobo, and use sentiment analysis to score the emotional value of many books. Compare that against a re-normalized distribution of books, to produce a machine that predicts how "good" a book is, against other positions in the dataset, from the written reviews of the book. This will need to bin out specific types of words/sentiments, and run classifications on them. 

Preferably, this can be interacted with by entering book title or isbn, and receive a book score based on the review. 

## Is it Wet Yet?

When it rains, people are aware of traffic slowdowns, but there are, in most cases, routes are not definate and chokepoints can be avoided. This project aims to use supervised learning algorithms to suggest the best routes to avoid conditional road congestion after identifying major choke points to avoid

This project would look at google maps data and city of austin traffic data, and cross it with weather data, then predict where the major slowdowns are, and, more interestingly, the high value alternative routes. 

Produce an API that reports to users, takes route information and calls to maps to source a route, then suggests detours around chokes


