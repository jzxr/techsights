#!/usr/bin/env python

#libraries
import praw
import pandas as pd
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod 
import schedule
import time
import json
import pytz
import csv
import tweepy
import re
import datetime
from datetime import timedelta
import schedule
import os
import unittest
#import tensorflow as tf

#Test Case

class testCases(unittest.TestCase):

    """Summary of testCases(unittest.TestCase) Function

    Description:
    This class has all the functions that performs unit testing.
    Unit testing is done to ensure program runs smoothly with no loopholes.

    """
    
    def testCase1 (self):
        
        """Summary of testCase1 (self) Function

        Description:
        Test if crawl time is float value & if subtraction method is correct

        """
        test = endTime - startTime
        
        if test == float and test == result:
            #assertTrue() to check true of test value
            self.assertTrue(test)
    
    
    def testCase2(self):

        """Summary of testCase2 (self) Function

        Description:
        Test if crawl time is lesser than 5 minutes

        """
        
        value1 = result
        value2 = 300
        
        #Error message in case if test case got failed 
        msg = "Crawl time is more than 5 minutes"
        
        #assert function() to check if values1 is less than value2 
        self.assertLess(value1, value2, msg) 
     
    
    def testCase3(self):

        """Summary of testCase3 (self) Function

        Description:
        Test if CSV file is created and stored in os.path

        """
        
        program = ['c_programming',"Python", "csharp", "javascript","html", "java","rprogramming"]
        
        for i in program:
            self.assertTrue(os.path.exists('reddit/reddit-' + i + '.csv'), "File does not exist!")
            self.assertTrue(os.path.exists('stackoverflow/stackoverflow-' + i + '.csv'), "File does not exist!")
            self.assertTrue(os.path.exists('github/github-' + i + '.csv'), "File does not exist!")
        
        twit = ["#ArtificialIntelligence", "#MachineLearning", "#DeepLearning", "#NeuralNetwork", "#DataScience",
                "#100DaysOfCode", "#DEVCommunity"]
        
        for t in twit:
            store = "_".join(re.findall(r"#(\w+)", t))
            #self.assertTrue(os.path.exists('twitter/recentpost/twitter_recent_' + store + '.csv'), "File does not exist!")
            self.assertTrue(os.path.exists('twitter/toppost/twitter_top_' + store + '.csv'), "File does not exist!")

            
    def testCase4(self):

        """Summary of testCase4 (self) Function

        Description:
        Test if folder contain correct number of files crawled 

        """
        
        expectedfiles=7
        # dir is your directory path
        list2=os.listdir("reddit")
        number_files2 = len(list2)
        self.assertEqual(number_files2,expectedfiles,'Number of files inserted not equal to 7 for reddit')
        
        list3=os.listdir("stackoverflow")
        number_files3 = len(list3)
        self.assertEqual(number_files3,expectedfiles,'Number of files inserted not equal to 7 for stackoverflow')
        
        list4=os.listdir("github")
        number_files4 = len(list4)
        self.assertEqual(number_files4,expectedfiles,'Number of files inserted not equal to 7 for github')
        
        onlyfiles1 = next(os.walk("twitter/recentpost"))[2] #dir is your directory path as string
        number_files1=len(onlyfiles1)
        self.assertEqual(number_files1,expectedfiles,'Number of files inserted not equal to 7 for twitter recent')
        
        onlyfiles = next(os.walk("twitter/toppost"))[2] #dir is your directory path as string
        number_files5=len(onlyfiles)
        self.assertEqual(number_files5,expectedfiles,'Number of files inserted not equal to 7 for twitter top')

        

#abstract class
class crawleddata(ABC):
    
    """Summary of crawleddata Function

    Description:
    This function is an abstract crawler class. It has the shared attributes defined within all the crawlers and abstract functions that will be defined
    properly in the individual subclasses.

    """

    def __init__(self,topic,df):

        """Summary of __init__(self,topic,df) Function

            Description:
            This is where the attributes of the parent class is defined. It takes in the parameters required to initiate the crawler which is the topic and dataframe.
            Self.data is empty as this is dependent on the aunthenticate functions in each subclass
            
            Parameters:
            self
            topic(str): the topic/hashtag to be crawled
            df(dataframe): empty dataframe for the crawler with only headers defined.

            Returns:
            None

        """
        self.topic = topic
        self.df = df
        self.data = None 
    
    def crawldatatop(self):
        """Summary of crawldatatop(self) Function

        Description:
        This is an abstract function that crawls the top data which is used by all the subclasses. This is left as abstract as each crawler sub class has different attributes that
        they crawl

        """
        pass
    
    def saveCV(self):
        """Summary of saveCV(self) Function

        Description:
        This is an abstract function that saves the dataframes into CSV. Naming convention is defined under each subclasses 
        """
        pass
    
    def authenticate(self):
        """Summary of saveCV(self) Function

        Description:
        This is an abstract function to authenticate into each social media. However, not all crawlers require authentication hence this can be used for pulling html and saving
        to self.data
        """
        pass

#reddit subclass
class crawledreddit(crawleddata):
    """Summary of crawledreddit Function

    Parameters:
    crawleddata(class): passes the parent class

    """

    def authenticate(self):
        
        """Summary of authenticate(self) Function

            Description:
            This functions authenticates into a valid reddit user with the specified id,secret,user_agent,username,password.
            The valid authentication is saved into the self.data attribute so that the whole session is authenticated by referring to this self.data
            
            Parameters:
            self

            Returns:
            self.data: returns the authenticated log in and saves into the self.data attribute

        """
        
        self.data = praw.Reddit(client_id='1Wbphu7sZiWpfg', client_secret='8SiX9MqF6468B9-8zTNBbAr3AZiAMg',
                                user_agent='dengueapp', username='assignmentproj', password='Password123')
        return self.data

    def crawldatatop(self):

        """Summary of crawldatatop(self) Function

            Description:
            This functions crawls the top reddit based on the self.topic that is specified during the creation of reddit instance.
            The crawled data is added to the originally empty dataframe based on the specified header.
            

            Parameters:
            self

            Returns:
            self.df: returns the updated dataframe with new crawled reddit entries

        """
        
        subreddit = self.data.subreddit(self.topic)
        top_subreddit = subreddit.top()
        for submission in top_subreddit:
            self.df = self.df.append({'Title': submission.title,
                            'Score':submission.score,
                            'ID':submission.id,
                           'URL':submission.url,
                           'Comms_num':submission.num_comments,
                           "Created":submission.created,
                           "Body":submission.selftext}, ignore_index=True)
        return self.df
    

    
    def crawldatasubtopic(self,subtopic):

        """Summary of crawldatasubtopic(self,subtopic) Function

            Description:
            This functions crawls the reddit subtopic within the specified self.topic that is specified during the creation of reddit instance.
            The crawled data is added to the originally empty dataframe based on the specified header.
            
            Parameters:
            self
            subtopic(str): takes in the value of the subtopic within a topic

            Returns:
            self.df: returns the updated dataframe with new crawled reddit entries

        """
        
        subreddit = self.reddit.subreddit(self.topic)
        top_subreddit = subreddit.search(subtopic)
        for submission in top_subreddit:
            self.df = self.df.append({'Title': submission.title,
                            'Score':submission.score,
                            'ID':submission.id,
                           'URL':submission.url,
                           'Comms_num':submission.num_comments,
                           "Created":submission.created,
                           "Body":submission.selftext}, ignore_index=True)
        return self.df
    
    def getsentiment(self):

        """Summary of getsentiment(self) Function

            Description:
            This functions adds a new column to the dataframe named 'Sentiment'. The Sentiment will check on the polarity of the body.
            A positive sentiment value = Positive Comment
            Zero sentiment value = Nuetral Comment
            A negative sentiment value = Negative Comment
            
            
            Parameters:
            self

            Returns:
            self.df: returns the updated dataframe with new crawled reddit entries

        """

        self.df['Sentiment'] = self.df['Body'].apply(lambda x: TextBlob(x).sentiment.polarity)
        self.df['Review'] = np.where(self.df['Sentiment']>=0, "Good","Bad")
        self.df['Nuetral'] = np.where(self.df['Sentiment']==0, "Nuetral","Not Nuetral")
        return self.df
    
    def cleandata(self):
        
        """Summary of cleandata(self) Function

            Description:
            This functions cleans up the dataframe by dropping irrelevant columns for easier analysis. It also creates 'Year' and 'Month' columns in case any time series
            would be used in the analysis.
            
            Parameters:
            self

            Returns:
            self.df: returns the updated dataframe with new crawled reddit entries

        """
        def get_date(created):
            return dt.datetime.fromtimestamp(created)
        _timestamp = self.df["Created"].apply(get_date)
        self.df = self.df.assign(timestamp = _timestamp)
        self.df = self.df.drop(['Created','Score','Comms_num'],axis=1)
        self.df['Year'] = pd.DatetimeIndex(self.df['timestamp']).year
        self.df['Month'] = pd.DatetimeIndex(self.df['timestamp']).month
        return self.df
    
    def saveCV(self):

        """Summary of saveCV(self) Function

            Description:
            This functions saves the dataframes into csv for use for analysis and for the front end.
            Local file storage is used as the program's database.
            It saves it in respective folders, if folder is not found, it will create a folder.
            
            Parameters:
            self

            Returns:
            None

        """
        
        if not os.path.exists('reddit'):
            os.makedirs('reddit')
        self.df.to_csv("reddit/reddit-" + self.topic + ".csv")

#stack overflow subclass
class stack(crawleddata):


    """Summary stack Function

    Parameters:
    crawleddata(class): passes the parent class

    """

    def authenticate(self):

        """Summary of authenticate(self) Function

            Description:
            Stack does not need proper authentication.
            This functions uses beautifulsoup4 to get the whole html page and save the data into self.data.
            
            Parameters:
            self

            Returns:
            self.data: returns the authenticated log in and saves into the self.data attribute

        """

        site = requests.get('https://stackoverflow.com/questions/tagged/'+self.topic); #recent question, other tags can be done as well
        soup = BeautifulSoup(site.text,"html.parser")
        self.data = soup.select(".question-summary")

    def crawldatatop(self):

        """Summary of crawldatatop(self) Function

            Description:
            This function seperates each entry within the whole html in self.data and splits it into the different rows and columns of the dataframe.
            The crawled data is added to the originally empty dataframe based on the specified header.
            

            Parameters:
            self

            Returns:
            self.df: returns the updated dataframe with new crawled stack entries

        """

        for question in self.data:
            self.df = self.df.append({'Title': question.select_one( '.question-hyperlink').get_text(),
                            'URL':question.select_one( '.question-hyperlink').get('href'),
                            'Views':question.select_one('.views').get('title'),
                           'Votes':question.select_one('.vote-count-post').get_text()}, ignore_index=True)
        self.df['URL'] = "https://stackoverflow.com" + self.df['URL'] 
        return self.df
                    
    def voterank(self):

        """Summary of voterank(self) Function

            Description:
            This function ranks the stack overflow entries based on the popularity of the views

            Parameters:
            self

            Returns:
            self.df: returns the updated dataframe with new crawled stack entries

        """
        
        self.df["Views"]= self.df['Views'].apply(lambda x: x[:2])
        self.df["Views"] = pd.to_numeric(self.df["Views"])
        self.df = self.df.sort_values(by='Views', ascending=False)
        return self.df
                            
    def saveCV(self):

        """Summary of saveCV(self) Function

            Description:
            This functions saves the dataframes into csv for use for analysis and for the front end.
            Local file storage is used as the program's database.
            It saves it in respective folders, if folder is not found, it will create a folder.
            
            Parameters:
            self

            Returns:
            None

        """
        
        if not os.path.exists('stackoverflow'):
            os.makedirs('stackoverflow')
        self.df.to_csv("stackoverflow/stackoverflow-" + self.topic + ".csv")

#github subclass
class crawledgithub(crawleddata):

    """Summary of crawledgithub Function

    Parameters:
    crawleddata(class): passes the parent class

    """
    
    def authenticate(self):

        """Summary of authenticate(self) Function

            Description:
            This functions authenticates into a valid stack overflow user with the specified access token.
            The valid authentication is saved into the self.data attribute so that the whole session is authenticated by referring to this self.data
            
            Parameters:
            self

            Returns:
            self.data: returns the authenticated log in and saves into the self.data attribute

        """
        
        self.data = "access_token=" + "cf0ff99540fe22c93255d736e3bed3bbfa10e17d"
        return self.data
        
    def crawldatatop(self):

        """Summary of crawldatatop(self) Function

            Description:
            This functions crawls the git hub entries based on the self.topic that is specified during the creation of github instance.
            The crawled data is added to the originally empty dataframe based on the specified header.
            Another column is created as well: Other Programming Languages URL to access all the languages present in the repository
            Calculation for the percentage of all the languages present in the repository is also done.
            

            Parameters:
            self

            Returns:
            self.df: returns the updated dataframe with new crawled reddit entries

        """
        
        #Range is set to 2 to shorten the search result
        for page in range(1, 2):
            #Building the Search API URL
            searchUrl = 'https://api.github.com/' + 'search/repositories?q=' + self.topic + '&page=' + str(page) + '&' + self.data

            #Get the requested searchURL
            response = requests.get(searchUrl).json()

            #Parse through the response of the searchQuery
            for item in response['items']:
                repository_name = item['name']
                repository_description = item['description']
                repository_stars = item['stargazers_count']
                repository_programming_language = item['language']
                repository_url = item['html_url']

                #Other Programming Languages URL to access all the languages present in the repository
                programming_language_url = item['url'] + '/languages?' + self.data
                programming_language_response = requests.get(programming_language_url).json()

                repository_other_languages = {}

                self.df = self.df.append({'Repository Name': repository_name, 'Description': repository_description,
                                 'Stars': repository_stars, 'Programming Language': repository_programming_language,
                                  'Other Language': repository_other_languages, 'URL': repository_url}, ignore_index=True)

                #Calculation for the percentage of all the languages present in the repository
                count_value = sum([value for value in programming_language_response.values()])
                for key, value in programming_language_response.items():
                    key_value = round((value / count_value) * 100, 2)
                    repository_other_languages[key] = key_value
        return self.df

    #Save CSV file
    def saveCV(self):
        """Summary of saveCV(self) Function

            Description:
            This functions saves the dataframes into csv for use for analysis and for the front end.
            Local file storage is used as the program's database.
            It saves it in respective folders, if folder is not found, it will create a folder.
            
            Parameters:
            self

            Returns:
            None

        """
        if not os.path.exists('github'):
            os.makedirs('github')
        self.df.to_csv("github/github-" + self.topic + ".csv")

#crawl Twitter
class crawledtwitter(crawleddata):

    """Summary Twitter Function

    Parameters:
    crawleddata(class): passes the parent class

    """
    
    def authenticate(self):

        """Summary of authenticate(self) Function

            Description:
            This functions authenticates into a valid twitter user with the specified Handler and access token.
            The valid authentication is saved into the self.data attribute so that the whole session is authenticated by referring to this self.data
            
            Parameters:
            self

            Returns:
            self.data: returns the authenticated log in and saves into the self.data attribute

        """
        
        auth = tweepy.OAuthHandler(
            "f9HugoUFnLlKdU4b6N2SFu8Ae",
            "zh7O2DYDdA4JN1Xe70PMaoHpslWQbNZnxsQzYRAUMx8LyuLb30",
        )
        auth.set_access_token(
            "1358278817085681665-szJPAYiD5uzRPyXDYamFnuwh2I2qoI",
            "fEh0d8l2b9kcL8jacPnVSRkleHAK30FS82spLYKSnCtKB",
        )

        # initialize Tweepy API
        self.data = tweepy.API(auth)
        return self.data

    def crawldatatop(self):

        """Summary of crawldatatop(self) Function

            Description:
            This function crawls the top tweets that matches the hashtag (self.topic).
            The crawled data is added to the originally empty dataframe based on the specified header.
            

            Parameters:
            self

            Returns:
            self.df: returns the updated dataframe with new crawled stack entries

        """
        
        # change createdAt from UTC to GMT+8
        timezone = pytz.timezone("Singapore")
        dateto = datetime.date.today()
        # for each tweet matching our hashtags, write relevant info to the spreadsheet
        for dayinput in range(-1, 7):
            for tweet in tweepy.Cursor(
                self.data.search,
                count=10,
                q=self.topic + "-filter:retweets",
                lang="en",
                until=dateto - timedelta(dayinput),
                include_entities=True,
                wait_on_rate_limit=True,
                tweet_mode="extended",
            ).items(10):
                if tweet.favorite_count != 0 and tweet.retweet_count != 0:
                    url = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
                    self.df = self.df.append(
                        {
                            "Tweet Content": tweet.full_text,
                            "User Name": tweet.user.screen_name,
                            "HashTags": [
                                e["text"] for e in tweet._json["entities"]["hashtags"]
                            ],
                            "Retweet Count": tweet.retweet_count,
                            "Favourite Count": tweet.favorite_count,
                            "URL": url,
                            "Created Date": tweet.created_at.date(),
                        },
                        ignore_index=True,
                    ).sort_values(
                        by=["Retweet Count", "Favourite Count"],
                        ascending=[False, False],
                    )
        return self.df

    
    def crawldatarecent(self):

        """Summary of crawldatatop(self) Function

            Description:
            This function crawls the recent tweets that matches the hashtag (self.topic).
            The crawled data is added to the originally empty dataframe based on the specified header.
            

            Parameters:
            self

            Returns:
            self.df: returns the updated dataframe with new crawled stack entries

        """
        
        # for each tweet matching our hashtags, write relevant info to the spreadsheet
        for tweet in tweepy.Cursor(
            self.data.search,
            q=self.topic + " -filter:retweets",
            lang="en",
            wait_on_rate_limit=True,
            tweet_mode="extended",
        ).items(100):
            url = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
            self.df = self.df.append(
                {
                    "Tweet Content": tweet.full_text,
                    "User Name": tweet.user.screen_name,
                    "HashTags": [
                        e["text"] for e in tweet._json["entities"]["hashtags"]
                    ],
                    "Retweet Count": tweet.retweet_count,
                    "Favourite Count": tweet.favorite_count,
                    "URL": url,
                },
                ignore_index=True,
            )
        return self.df

    def saveCV(self, name):

        """Summary of saveCV(self) Function

            Description:
            This functions saves the dataframes into csv for use for analysis and for the front end.
            Local file storage is used as the program's database.
            It saves it in respective folders, if folder is not found, it will create a folder.
            
            Parameters:
            self

            Returns:
            None

        """

        
        if not os.path.exists('twitter'):
            os.makedirs('twitter')
        if name == "r":
            if not os.path.exists('twitter/recentpost'):
                os.makedirs('twitter/recentpost')
            fname = "_".join(re.findall(r"#(\w+)",self.topic))
            self.df.to_csv("twitter/recentpost/twitter_recent_" + fname+".csv")
        else:
            if not os.path.exists('twitter/toppost'):
                os.makedirs('twitter/toppost')
            fname = "_".join(re.findall(r"#(\w+)",self.topic))
            self.df.to_csv("twitter/toppost/twitter_top_" + fname+".csv")
    

#creating dfs and initializing
class task():
    def runtask():
        """Summary Twitter Function

        Description:
        This function is made to allow main function to be clean. Hence, all the task that needs to be run is within this class and function.
        Dataframe for each crawler is predefined here.
        Array of topics to be crawled is also defined here.
        Instances of each crawler objects are defined here as well.

        """
        
        df = pd.DataFrame(columns=['Title','Score','ID','URL','Comms_num','Created','Body'])
        df1 = pd.DataFrame(columns=['Title','URL','Views','Votes'])
        df3 = pd.DataFrame(columns=['Repository Name', 'Description', 'Stars','Programming Language', 'Other Language', 'URL'])
        df4 = pd.DataFrame(columns=['Tweet Content','User Name','HashTags','Retweet Count','Favourite Count','URL'])
        df5 = pd.DataFrame(columns=['Tweet Content','User Name','HashTags','Retweet Count','Favourite Count','URL','Created Date'])
                
        #enquiring languages
        languages = ['c_programming',"Python", "csharp", "javascript","html", "java","rprogramming"]


        print(crawledreddit.authenticate.__doc__)

        for i in languages:
            stackoverflow = stack(i,df1)
            stackoverflow.authenticate()
            stackoverflow.crawldatatop()
            stackoverflow.voterank()
            stackoverflow.saveCV()
        print("Stack has been crawled!")
        
        for i in languages:
            
            redditdata = crawledreddit(i,df)
            redditdata.authenticate()
            redditdata.crawldatatop()
            redditdata.cleandata()
            redditdata.getsentiment()
            redditdata.saveCV()
        print("Reddit has been crawled!")

  

        for i in languages:
            github = crawledgithub(i,df3)
            github.authenticate()
            github.crawldatatop()
            github.saveCV()
        print("Github has been crawled!") 
        #enquiring trends
    
        trends = [
            "#ArtificialIntelligence",
            "#MachineLearning",
            "#DeepLearning",
            "#NeuralNetwork",
            "#DataScience",
            "#100DaysOfCode",
            "#DEVCommunity",
        ]
        
        #for recent tweets
        for i in trends:
            recenttweets = crawledtwitter(i,df4)
            recenttweets.authenticate()
            recenttweets.crawldatarecent()
            recenttweets.saveCV("r")
        print("Recent tweets has been crawled!")
         #for top tweets
        for i in trends:
            recenttweets = crawledtwitter(i,df5)
            recenttweets.authenticate()
            recenttweets.crawldatatop()
            recenttweets.saveCV("t")
        print("Top tweets has been crawled!")
        
#main program
if __name__ == "__main__":
    print("Welcome to our Programming Language/Trend Crawler\n")

    startTime = time.perf_counter()
    task.runtask()
    endTime = time.perf_counter()
    result = endTime - startTime
    print (f"Total time taken to webcrawl is {result:0.4f} seconds!")
    schedule.every(1).minutes.do(task.runtask)
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    while True:
        schedule.run_pending()
        time.sleep(1)


# In[ ]:




