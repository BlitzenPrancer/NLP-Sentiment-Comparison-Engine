import tweepy
from textblob import TextBlob
import preprocessor as p
import statistics
from typing import List

# downloading real time tweets

# creating secret key and secret file to store consumer_key and consumer_secret
consumer_key = "LpGzyBpcmARgNZSNrArg95jZK"
consumer_secret = "WTzQpSw6FWjC5FBC23LBSaajWXKeDpo31YwPln0jteS9s2Hgwn"
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)


# getting tweets
# it is going to take keyword string and returns list of strings
def get_tweets(keyword: str) -> List[str]:
    all_tweets = []
    for tweet in tweepy.Cursor(api.search, q = keyword, tweet_mode = 'extended', lang = 'en').items(10):
        all_tweets.append(tweet.full_text)

    return all_tweets

# cleaning the tweets with preprocessor library
def clean_tweets(all_tweets: List[str]) -> List[str]:
    tweets_clean = []
    for tweet in all_tweets:
        tweets_clean.append(p.clean(tweet))

    return tweets_clean

# passing the cleaned tweets to get_sentiment() function
# This function returns the sentiment scores of each of our 10 tweets
def get_sentiment(all_tweets: List[str]) -> List[float]:
    sentiment_scores = [] # this holds scores for each tweet
    # using TextBlob library to generate the polarity sentiment scores
    for tweet in all_tweets:
        blob = TextBlob(tweet)
        sentiment_scores.append(blob.sentiment.polarity)

    return sentiment_scores

# generating average sentiment score for all the tweets we have downloaded
# we want to have average scores for all of the 10 tweets
# so that we can have a view/picture of what is the sentiment for this keyword at this very moment in time
def generate_average_sentiment_score(keyword: str) -> int:
    tweets = get_tweets(keyword)
    tweets_clean = clean_tweets(tweets)
    sentiment_score = get_sentiment(tweets_clean)

    # calculating average score using statistics
    average_score = statistics.mean(sentiment_score)
    return average_score

if __name__ == "__main__":
    print("Whom does the world prefer the most?")
    first_one = input()
    print("...or...")
    second_one = input()
    print("\n")
    first_score = generate_average_sentiment_score(first_one)
    second_score = generate_average_sentiment_score(second_one)

    if (first_score > second_score):
        print(f"The world needs {first_one} over {second_one}!")
    else:
        print(f"The world needs {second_one} over {first_one}!")