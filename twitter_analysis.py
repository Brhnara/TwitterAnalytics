# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 12:50:06 2019

@author: LENOVO
"""
from warnings import filterwarnings
filterwarnings ('ignore')
import pandas as pd
import numpy as np
import tweepy,codecs

consumer_key=''
consumer_secret=''
acces_token=''
access_token_secret=''

#Connection to twitter

auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(acces_token,access_token_secret)
api=tweepy.API(auth)

#check connection
api.update_status("Hello from Python")

#fetching data 


me=api.me() 
me.screen_name
me.followers_count
me.friends

user=api.get_user(id=" ")
user.screen_name
user.followers_count
user.profile_image_url

#home timeline
public_tweets=api.home_timeline(count=5)
for tweet in public_tweets:
    print(tweet.text)
    
#user timeline
name=" " 
tweet_count=10
user_timeline=api.user_timeline(id=name,count=tweet_count)
for i in user_timeline:
    print(i.text)   

#retweeted 
retweets=api.retweets_of_me(count=3)
for i in retweets:
    print(i.text)
    
#hashtag fetch
results=api.search(q=" ",lang=" ",result_type="recent",count=10)
for tw in results:
    print(tw.text)    

#data frame
def tweets_df(results):
    id_list = [tweet.id for tweet  in results]
    import pandas as pd
    data_set = pd.DataFrame(id_list, columns = ["id"])
    
    data_set["text"] = [tweet.text for tweet in results]
    data_set["created_at"] = [tweet.created_at for tweet in results]
    data_set["retweet_count"] = [tweet.retweet_count for tweet in results]
    data_set["user_screen_name"] = [tweet.author.screen_name for tweet in results]
    data_set["user_followers_count"] = [tweet.author.followers_count for tweet in results]
    data_set["user_location"] = [tweet.author.location for tweet in results]
    data_set["Hashtags"] = [tweet.entities.get('hashtags') for tweet in results]
    
    return data_set

data=tweets_df(results)

#data["text"]

data.to_csv("data_twitter.csv")


#profile analysis

tweets = api.user_timeline(id = " ")

for i in tweets:
    print(i.text)

def timeline_df(tweets):
    idler = [tweet.id for tweet  in tweets]
    import pandas as pd
    df = pd.DataFrame(idler, columns = ["id"])
    
    df["created_at"] = [tweet.created_at for tweet in tweets]
    df["text"] = [tweet.text for tweet in tweets]
    df["favorite_count"] = [tweet.favorite_count for tweet in tweets]
    df["retweet_count"] = [tweet.retweet_count for tweet in tweets]
    df["source"] = [tweet.source for kisi in tweets]
    
    return df

time_linedf(tweets)

tweets=api.user_timeline(id=" ",count=200)
df=timeline_df(tweets)

df.shape
df.head()

df.sort_values("favorite_count",ascending=False)
df.sort_values("retweet_count",ascending=False)

#Retweet and Favorites distrubution


import seaborn as sns
import matplotlib.pyplot as plt

sns.distplot(df.favorite_count, kde = False, color = "blue");

sns.distplot(df.retweet_count, color = "blue");

plt.xlim(-100, 5000)

#Tweet-hour-day distrubution

df["tweet_hour"] = df["created_at"].apply(lambda x: x.strftime("%H"))
df.head()

df["tweet_hour"] = pd.to_numeric(df["tweet_hour"])
df.info()
sns.distplot(df["tweet_hour"], kde = False, color ="blue");

df["days"] = df["created_at"].dt.weekday_name
df.head()

day_freq = df.groupby("days").count()["id"]
day_freq.plot.bar(x = "days", y = "id")
    
#tweet source

source_freq = df.groupby("source").count()["id"]
source_freq.plot.bar(x = "source", y = "id")
df.groupby("source").count()["id"]
df.groupby(["source","tweet_hour","days"])[["tweet_hour"]].count()


#Followers and friends analysis

user = api.get_user(id = " ")
for friend in user.friends():
    print(friend.screen_name)
    
friends = user.friends()
followers = user.followers()

def followers_df(flwrs):
    
    idler = [i.id for i  in flwrs]
    df = pd.DataFrame(idler, columns = ["id"])
    
    df["created_at"] = [kisi.created_at for kisi in flwrs]
    df["screen_name"] = [kisi.screen_name for kisi in flwrs]
    df["location"] = [kisi.location for kisi in flwrs]
    df["followers_count"] = [kisi.followers_count for kisi in flwrs]
    df["statuses_count"] = [kisi.statuses_count for kisi in flwrs]
    df["friends_count"] = [kisi.friends_count for kisi in flwrs]
    df["favourites_count"] = [kisi.favourites_count for kisi in flwrs]
    
    return df

df = followers_df(followers)
df.head()


#follower segmentation


df.index = df["screen_name"]
s_data = df[["followers_count", "statuses_count"]]

s_data = s_data.apply(lambda x: (x-min(x))/(max(x)-min(x))) #standardization

s_data["followers_count"] = s_data["followers_count"] + 0.01
s_data["statuses_count"] = s_data["statuses_count"] + 0.01
s_data.head()
skor = s_data["followers_count"] * s_data["statuses_count"]
skor.sort_values(ascending = False)
skor[skor > skor.median() + skor.std()/len(skor)].sort_values(ascending = False)

s_data["segment"] = np.where(s_data["skor"] >= skor.median() + 
                             skor.std()/len(skor), "A","B")


