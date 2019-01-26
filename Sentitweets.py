
"""PROJECT: TWITTER SENTIMENT ANALYSIS
   Author: SHRAY MISHRA
   LIBRARIES USED: PANDAS, NUMPY, MATPLOTLIB, SEABORN, TEXTBLOB, TWEEPY
"""

'''import pip
package_name='tweepy' 
pip.main(['install',package_name])'''


# Importing necessary libraries

import pandas as pd     # For data handing
import numpy as np      # For computation
import tweepy            # Twitter library

# For plotting and visualization:
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sea

# Using credentials which will give access to Tweets:
from credentials import *    

# Let's setup Twitter API:
def twitter_API():
    
    # Authentication through developer account keys:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    # Returns API along with authentication:
    api = tweepy.API(auth)
    

# Created an object called feeder to run method "twitter_API"
feeder = twitter_API()

""" ANALYSIS OF INFORMATION CONTAINED IN LATEST 200 TWEETS"""

# Taking input Twitter Username and printing out the number of tweets

tweets = feeder.user_timeline(screen_name="BarackObama", count=200)
print(f'Number of tweets: {len(tweets)}.\n')

print (f"Latest Five Tweets :")
[print(tweet.text) for tweet in tweets[:5]]

# Returns the follower_ids of the user in an array    
print (feeder.followers_ids(screen_name = "BarackObama"))

# Created a dataframe using pandas:
twitter_data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

# First twenty elements of the dataframe:
display(twitter_data.head(20))

# Displays available methods for a single tweet object:
# print(dir(tweets[0]))


# Details about the first tweet:
print(f'This Tweet was sent on : {tweets[0].created_at}')
print(f'Number of times favorited: {tweets[0].favorite_count}')
print(f'Number of times retweeted: {tweets[0].retweet_count}')
print(f'Source of this tweet is: {tweets[0].source}')
print(f'Geographical location of user if allowed: {tweets[0].geo}')
print(f'Coordinates of user if allowed: {tweets[0].coordinates}')
# print(f'Various Entities associated with this tweet are:{tweets[0].entities}')

# Deriving useful data and adding to dataframe:

twitter_data['ID']   = np.array([tweet.id for tweet in tweets])
twitter_data['Date'] = np.array([tweet.created_at for tweet in tweets])
twitter_data['Medium'] = np.array([tweet.source for tweet in tweets])
twitter_data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
twitter_data['RTs']    = np.array([tweet.retweet_count for tweet in tweets])
twitter_data['len']  = np.array([len(tweet.text) for tweet in tweets])



# Tweet with most favourites and most retweets:

most_fav = np.max(twitter_data['Likes'])
most_RT  = np.max(twitter_data['RTs'])

liked = twitter_data[twitter_data.Likes == most_fav].index[0]
retweeted  = twitter_data[twitter_data.RTs == most_RT].index[0]

# Most liked tweets:

print(f"Most liked tweet is: {(twitter_data['Tweets'][liked])}")
print(f"Number of likes: {(most_fav)}")


# Most Retweeted tweets:

print(f"Most retweeted tweet is: {(twitter_data['Tweets'][retweeted])}")
print(f"Number of retweets: {(most_RT)}")

# Calculating mean tweet lenght:

mean = np.mean(twitter_data['len'])

print (f'The average lenght of tweets are: {mean}')

# Finding medium for tweets (Like iPhone, Android):

medium = []
for i in twitter_data['Medium']:
    if i not in medium:
        medium.append(i)

# List of all medium for tweets:

print("Medium of sending tweets:")
for i in medium:
    print(f"{medium}")

# Vector creation:

col = np.zeros(len(medium))

for i in twitter_data['Medium']:
    for j in range(len(medium)):
        if i == medium[j]:
            col[j] += 1
            pass

col /= 100

# Time series Analysis of twitter data:

ts = pd.Series(data = twitter_data['len'].values, index=twitter_data['Date'])
ts_like = pd.Series(data = twitter_data['Likes'].values, index = twitter_data['Date'])
ts_RT = pd.Series(data = twitter_data['RTs'].values, index= twitter_data['Date'])




"""          SENTIMENT ANALYSIS BEGINS
           LIBRARY USED : TEXTBLOB, REGEX  """

from textblob import TextBlob
import re

# Function for cleaning tweets by removing urls and special character

def clean(tweet):
    
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


# Function for calculating the polarity in tweets using textblob
    
def sentimentanalysis(tweet):
    
    sentanalysis = TextBlob(clean(tweet))
    if sentanalysis.sentiment.polarity > 0:
        return 1
    elif sentanalysis.sentiment.polarity == 0:
        return 0
    else:
        return -1

# Sentiment Analysis Results in numpy array:
        
twitter_data['SentiAnalysis'] = np.array([sentimentanalysis(tweet) for tweet in twitter_data['Tweets'] ])

# Showing the updated dataframe:

display(twitter_data.head(20))


# Dividing Tweets in lists based on polarity:

positive = [ tweet for position, tweet in enumerate(twitter_data['Tweets']) if twitter_data['SentiAnalysis'][position] > 0]
neutral = [ tweet for position, tweet in enumerate(twitter_data['Tweets']) if twitter_data['SentiAnalysis'][position] == 0]
negative = [ tweet for position, tweet in enumerate(twitter_data['Tweets']) if twitter_data['SentiAnalysis'][position] < 0]

# Sentiment Analysis through Percentage:

print(f"Positive tweet percentage: {len(positive)*100/len(twitter_data['Tweets'])}%")
print(f"Neutral tweet percentage: {len(neutral)*100/len(twitter_data['Tweets'])}%")
print(f"Negative tweet percentage: {len(negative)*100/len(twitter_data['Tweets'])}%")

# Graphical representation of the outputs      
      
# Plotting the lenght with time:

ts.plot (figsize= (20,6), color='b', label = 'Time Series Analysis of Twwet Length');

# Likes and Retweets Plots:

ts_like.plot(figsize= (20,6), label= "Likes", legend=True)
ts_RT.plot(figsize=(20,6), label = "Retweets", legend=True);

# Plotting the medium share in pie chart:

chart = pd.Series(col, index = medium, name = 'Medium')
chart.plot.pie(fontsize=15, autopct='%.4f', figsize=(10, 10));

